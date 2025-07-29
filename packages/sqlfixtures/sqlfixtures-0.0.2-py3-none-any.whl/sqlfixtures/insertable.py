import inspect
import contextlib
import logging
import operator

import typing as t
from typing import Any
from typing import Iterable
from typing import Mapping
from typing import Generator
from typing import overload
from inspect import Parameter
from functools import partial
from itertools import chain

from sqlfixtures.sqlfixture import SQLFixture
from sqlfixtures.sqlfixture import AttrDict

__all__ = ["Insertable", "apply_to_fixture", "Generated", "SELF", "PARENT"]
logger = logging.getLogger(__name__)

RowType: t.TypeAlias = AttrDict


class Insertable:
    """
    Describe a single record to be inserted.

    :class:`sqlfixture.Insertable` objects are instantiated with the name of
    the table they insert into, and keyword args describing column values::

        user = Insertable(
            "users",
            username="user1@example.com",
            email="user1@example.com",
        )



    Insertables can reference other insertables::

        class sqlfixture:
            user = Insertable("users", name="bernice")
            post = Insertable("posts", content="...", user_id=user.id)

    Use sqlfixtures.insertable.SELF for access to the current Insertable::

        class sqlfixture:
            post = Insertable(
                "posts",
                content="...",
                owner=Insertable("users", name="bernice"),
                owner_id=SELF.owner.id
            )
    """

    _items: dict[str, Any]
    _after: dict[str, Any]
    _attributes: list[tuple[str, str]]
    _lookup: dict[type, str] = {}
    _parent: "Reference | Insertable"
    table: str

    def __init__(self, *args: Any, **kwargs: Any):
        self.__dict__["_items"] = {}
        self.__dict__["_after"] = {}
        self.__dict__["_parent"] = SELF._parent
        self.__dict__["_attributes"] = []
        match args:
            case (str(s),):
                self.__dict__["table"], what = s, {}
            case (str(t), w):
                self.__dict__["table"], what = t, w
            case (x,):
                what = x
                self.__dict__["table"] = self.__class__._lookup[type(what)]
            case _:
                what = None

        items = {}
        match what:
            case None:
                pass
            case dict(mapping):
                items = mapping
            case _:
                items = dict(inspect.getmembers(what))

        items = items | kwargs
        for k, v in items.items():
            if callable(v) and not isinstance(v, (Insertable, Reference)):
                v = Generated(v, self)
            elif isinstance(v, Generated):
                v.set_insertable(self)
            self[k] = v
        assert "_parent" not in self._items

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.table} {repr(self._items)[:40]}...>"

    def __getattr__(self, name):
        try:
            value = self._items[name]
        except KeyError:
            return getattr(Reference(self), name)
        return value

    def __setattr__(self, name, what):
        if isinstance(what, Insertable):
            what.set_parent(self)
        if _is_insertable_list(what):
            what = t.cast(Iterable[Insertable], what)
            for item in what:
                item.set_parent(self)

        self._items[name] = what

    def set_parent(self, parent):
        object.__setattr__(self, "_parent", parent)

    def __getitem__(self, name):
        return self._items[name]

    def __setitem__(self, key, what):
        if "__" in key:
            base, rest = key.split("__", 1)
            if base in self._items:
                self._items[base][rest] = what
            else:
                raise AttributeError(base)

        else:
            self.__setattr__(key, what)

    def __iter__(self) -> t.Iterator[str]:
        return iter(self._items)

    def __call__(self, *args, **kw) -> "Insertable":
        """
        Return a new Insertable based on the current object, updated with the
        given table and/or items.
        """
        match args:
            case []:
                table, items = (self.table, self._items)
            case (str(s), w):
                table, items = (s, self._items | self.w)
            case (str(s),):
                table, items = (s, self._items)
            case (w,):
                table, items = self.table, self._items | w
            case _:
                raise ValueError(f"Invalid args {args=}")

        def copy_items(items):
            copied_items = {}
            for k, v in items.items():
                if isinstance(v, Insertable):
                    copied_items[k] = v()
                elif _is_insertable_list(v):
                    copied_items[k] = [child() for child in v]
                else:
                    copied_items[k] = v
            return copied_items

        copy = self.__class__(table, copy_items(items), **kw)
        if self._after:
            object.__setattr__(copy, "_after", copy_items(self._after))
        return copy

    def __or__(self, items) -> "Insertable":
        """
        Return a new Insertable based on the current object, updated with the
        given items.
        """
        return self(items)

    @classmethod
    def as_dict(cls, instance):
        return instance._items.copy()

    @classmethod
    def unresolved(cls, instance):
        """
        Return all attributes referring to other Insertables, which must be
        resolved before this insertable can be inserted.
        """
        return ((k, v) for k, v in instance._items.items() if isinstance(v, Reference))

    def items(self):
        return self._items.items()

    def after(self, **kwargs):
        """
        Add items to be updated after insertion. Typically used to break
        circular dependencies.

        For example, the following code would cause an unresolvable loop::

            Insertable(
                "foo",
                bar_id=Insertable("bar", foo_id=PARENT.id).id
            )

        This could be rewritten as::

            Insertable(
                "foo",
                bar=Insertable("bar", foo_id=PARENT.id)
            ).after(bar_id=SELF.bar.id)
        """
        for k, v in kwargs.items():
            if callable(v) and not isinstance(v, (Insertable, Reference)):
                v = Generated(v, self)
            elif isinstance(v, Generated):
                v.set_insertable(self)
            self._after[k] = v
        return self

    def is_resolvable(self, resolved: set["Insertable"]) -> bool:
        """
        Return True if all items in the Insertable are
        able to be resolved to values that can be inserted.
        """
        for item in self._items.values():
            if isinstance(item, Reference) and item.source not in resolved:
                logger.info(
                    f"{self} is not resolvable because {item!r} is not resolved"
                )
                return False

        return True

    @classmethod
    def map_type(cls, type_, table):
        """
        Map a type to a specific table
        """
        cls._lookup[type_] = table

    @classmethod
    def self(cls):
        """
        Return an unresolved object that points to an attribute on the
        containing object. Used when you have a parent-child relationship, for
        example::

            post = Insertable(
                "posts",
                title="Post title",
                owner=Insertable("user", name="Allison Author"),
                owner_id=Insertable.self().owner.id
            )

        """
        return Reference.self()

    def flatten(self):
        """
        Given an Insertable, traverse any child Insertables in a depth-first order,
        generating the list of Insertables traversed.
        """
        for v in self._items.values():
            if isinstance(v, Insertable):
                yield from v.flatten()
            elif _is_insertable_list(v):
                for child in v:
                    yield from child.flatten()
        yield self

    @classmethod
    def insert(
        cls,
        conn,
        items: Iterable["Insertable"] | Mapping[str, "Insertable"] | type,
        commit: bool = False,
    ) -> contextlib.AbstractContextManager[dict[str, Any] | list[Any] | Any]:
        """
        Create a SQLFixture that inserts the given Insertables,
        and returns the inserted rows either as a list, dict or namedtuple, to
        match the input type
        """
        fixture = SQLFixture(conn)
        return apply_to_fixture(fixture, items, commit=commit)


T = t.TypeVar("T")


class Generated(t.Generic[T]):
    insertable: Insertable

    @overload
    def __init__(
        self,
        fn: t.Callable[[Insertable], t.Any],
        insertable: t.Optional[Insertable] = None,
    ):
        ...

    @overload
    def __init__(
        self, fn: t.Callable[[], t.Any], insertable: t.Optional[Insertable] = None
    ):
        ...

    def __init__(self, fn, insertable=None):
        self.fn = fn
        self.pass_insertable = False
        if insertable:
            self.set_insertable(insertable)
        try:
            sig = inspect.signature(fn)
        except ValueError:
            # Some callables will fail, eg builtins.next.
            #
            # A common pattern is to do::
            #
            #   Insertable(..., column=partial(next, itertools.count()))
            #
            # so set pass_insertable to false to ensure this works.
            self.pass_insertable = False
        else:
            params = list(sig.parameters.values())
            self.pass_insertable = (
                len(params) > 0
                and params[0].kind
                in {Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD}
                and params[0].default is Parameter.empty
            )

    def set_insertable(self, insertable: Insertable):
        self.insertable = insertable

    def __call__(self) -> T:
        if self.pass_insertable:
            return self.fn(self.insertable)
        else:
            return self.fn()


class Reference:
    """
    A reference to an unresolved object or property.
    """

    #: Indicate that the source is the parent object itself
    SELF = object()

    def __init__(self, source=SELF, attrs=None):
        self.source = source
        self.attrs = attrs if attrs else []

    def __repr__(self):
        source = "self" if self.source is self.SELF else self.source
        return (
            f"<{self.__class__.__name__} "
            f"{source}.{'.'.join(str(k) for _, k in self.attrs)}>"
        )

    def __getattr__(self, key):
        return self.__class__(self.source, self.attrs + [(operator.attrgetter, key)])

    def __getitem__(self, key):
        return self.__class__(self.source, self.attrs + [(operator.itemgetter, key)])

    def with_source(self, source) -> "Reference":
        return self.__class__(source, self.attrs)

    def unpeel(self) -> tuple[Any, "Reference | None"]:
        """
        Dereference the first layer of the referenced object and return it
        alongside a new Reference object containing the remainder of the
        referenced path.

        If no more layers of reference remain, the returned Reference is
        None.
        """
        if self.source is self.SELF:
            raise ValueError("Source is not set")

        (op, key), remaining_attrs = self.attrs[0], self.attrs[1:]
        referenced = op(key)(self.source)
        if not remaining_attrs:
            return referenced, None
        return referenced, self.__class__(referenced, remaining_attrs)

    @classmethod
    def self(cls):
        return cls(cls.SELF)


SELF = Reference.self()
PARENT = SELF._parent


@overload
def apply_to_fixture(
    fixture: SQLFixture,
    items: Mapping[str, Insertable],
    commit: bool = False,
    revert: bool = True,
) -> contextlib.AbstractContextManager[RowType]:
    ...


@overload
def apply_to_fixture(
    fixture: SQLFixture,
    items: Iterable[Insertable],
    commit: bool = False,
    revert: bool = True,
) -> contextlib.AbstractContextManager[list[RowType]]:
    ...


@overload
def apply_to_fixture(
    fixture: SQLFixture, items: type, commit: bool = False, revert: bool = True
) -> contextlib.AbstractContextManager[Any]:
    ...


@contextlib.contextmanager
def apply_to_fixture(
    fixture: SQLFixture,
    items: Mapping[str, Insertable] | Iterable[Insertable] | type,
    commit: bool = False,
    revert: bool = True,
) -> t.Union[
    Generator[RowType, None, None],
    Generator[list[Any], None, None],
    Generator[Any, None, None],
]:
    make_result: t.Callable[[RowType], Any]
    if isinstance(items, Mapping):

        def make_result_mapping(inserted):
            return inserted

        make_result = make_result_mapping

    elif isinstance(items, Iterable):
        items = t.cast(
            dict[str, Insertable], {str(ix): ins for ix, ins in enumerate(items)}
        )

        def make_result_iterable(inserted):
            return [inserted[k] for k in sorted(inserted)]

        make_result = make_result_iterable

    elif isinstance(items, type):
        instance = items()
        items = t.cast(
            dict[str, Insertable],
            {k: v for k, v in inspect.getmembers(items) if isinstance(v, Insertable)},
        )

        def make_result_type(inserted):
            for k in inserted:
                setattr(instance, k, inserted[k])
            return instance

        make_result = make_result_type

    generator = _apply_to_fixture(fixture, items, commit, revert)
    value = next(generator)
    result = make_result(value)
    yield result


def _apply_to_fixture(
    fixture, items: Mapping[str, Insertable], commit: bool = False, revert: bool = True
) -> Generator[RowType, None, None]:
    """
    Apply a dict containing :class:`sqlfixtures.insertable.Insertable`
    to a fixture, returning the created items as an AttrDict.

    Example::

        with apply_to_fixture(
            SQLFixture(conn),
            {"user": Insertable("user", name="Hank")}
        ) as items:
            # ``items`` is now a dict reflecting the original inputs, ie:
            # {"user": <User>}
            ...

    """
    insertable_row_map: dict[Insertable, RowType] = {}
    relations: list[
        tuple[
            RowType,
            list[tuple[str, t.Callable[[], RowType]]],
        ]
    ] = []
    afters: list[tuple[RowType, Insertable]] = []

    name_map = {insertable: name for name, insertable in items.items()}
    to_insert = list(chain.from_iterable(ins.flatten() for ins in items.values()))
    with contextlib.ExitStack() as stack:
        relations = []
        while to_insert:
            unresolved: list[Insertable] = []
            for insertable in to_insert:
                insert_values = {}
                _relations: list[
                    tuple[str, t.Callable[[], RowType | list[RowType]]]
                ] = []
                try:
                    for k, v in insertable.items():
                        if isinstance(v, Insertable):
                            _relations.append(
                                (k, partial(operator.itemgetter(v), insertable_row_map))
                            )
                        elif _is_insertable_list(v):
                            _relations.append(
                                (
                                    k,
                                    lambda v=v: [
                                        insertable_row_map[child] for child in v
                                    ],
                                )
                            )
                        else:
                            insert_values[k] = dereference(
                                insertable, v, insertable_row_map
                            )
                except DereferenceError:
                    unresolved.append(insertable)
                    continue

                if insertable in insertable_row_map:
                    raise AssertionError("Seen {insertable=} twice!")
                insertable_row_map[insertable] = row = stack.enter_context(
                    fixture.insert(insertable.table, insert_values, commit, revert)
                )
                if insertable._after:
                    afters.append((row, insertable))
                if _relations:
                    relations.append((row, _relations))

            if len(to_insert) == len(unresolved):
                raise AssertionError(f"Can't resolve all insertables: {unresolved=}")
            to_insert = unresolved

        for row, insertable in afters:
            update_values = {
                k: dereference(insertable, v, insertable_row_map)
                for k, v in insertable._after.items()
            }
            key_values = {k: v for k, v in row.items() if k not in update_values}
            stack.enter_context(
                fixture.update(
                    insertable.table,
                    values=update_values,
                    where=key_values,
                    revert=revert,
                )
            )
            row.update(update_values)

        for row, relation_items in relations:
            for k, v in relation_items:
                row[k] = v()

        yield AttrDict(
            {
                name: insertable_row_map[insertable]
                for insertable, name in name_map.items()
            }
        )


def _is_insertable_list(v: t.Any) -> bool:
    return bool(
        v
        and not isinstance(v, (str, bytes))
        and isinstance(v, Iterable)
        and all(isinstance(child, Insertable) for child in v)
    )


def dereference(source, ref, insertable_row_map):
    if isinstance(ref, Generated):
        return dereference(source, ref(), insertable_row_map)
    elif isinstance(ref, Reference):
        if ref.source is ref.SELF:
            ref = ref.with_source(source)
        original_ref = ref
        ob = source
        while isinstance(ref, Reference):
            ob, ref = ref.unpeel()

        if isinstance(ob, Reference):
            if ob.source in insertable_row_map:
                ob, ref = ob.with_source(insertable_row_map[ob.source]).unpeel()

            else:
                raise DereferenceError(
                    f"{ob.source!r} via {original_ref!r} does not have yet any row data"
                )

        elif ob in insertable_row_map:
            ob = insertable_row_map[ob]
        assert not isinstance(ob, (Reference, Insertable))
        return dereference(source, ob, insertable_row_map)
    else:
        return ref


class DereferenceError(BaseException):
    """
    A Reference could not be dereferenced
    """
