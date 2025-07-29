import contextlib
from uuid import uuid1

from typing import Any
from typing import Mapping
from typing import Iterable
from typing import Sequence
from typing import Generator

from embrace.query import Query

RowType = Mapping | Sequence[tuple[str, Any]]


class SQLFixture:
    """
    Usage::

        conn = sqlite3.connect(...)
        sqlf = SQLFixture(conn)

        with sqlf.insert("user", {"name": "Angus", email="angus@example.com"}) as user:
            assert user.name == "Angus"

    """

    _supports_returning = None

    class Literal(str):
        """
        A string to be inserted into the sql statement as a literal (no quoting)
        """

    def __init__(self, conn):
        self.conn = conn

    @property
    def supports_returning(self) -> bool:
        if self._supports_returning is None:
            with savepoint(self.conn) as savepoint_name:
                cursor = self.conn.cursor()
                cursor.execute(
                    f"CREATE TEMPORARY TABLE _tmp_{savepoint_name} (x char(1))"
                )
                try:
                    cursor.execute(
                        f"INSERT INTO _tmp_{savepoint_name} VALUES ('a') RETURNING *"
                    )
                    self._supports_returning = tuple(cursor.fetchone()) == ("a",)
                except Exception:
                    self._supports_returning = False
        return self._supports_returning

    @contextlib.contextmanager
    def insert(
        self,
        table: str,
        row: RowType | None = None,
        commit=False,
        revert=True,
        **kwargs,
    ) -> Generator["AttrDict", None, None]:
        if row is None:
            row = kwargs
        else:
            row = dict(row, **kwargs)
        if not row:
            raise AssertionError("row cannot be empty")
        with self.insert_many(table, [row], commit=commit, revert=revert) as result:
            yield result[0]

    @contextlib.contextmanager
    def insert_many(
        self, table: str, rows: Iterable[Mapping], commit=False, revert=True
    ) -> Generator[list["AttrDict"], None, None]:
        """
        :param table:
            table in which to insert rows
        :param rows:
            an iterable of row data. Each row should be a mapping from
            fieldnames to values
        :param commit:
            commit to the database after the initial insert, and again after
            deletion
        :param revert:
            if true, rows will be deleted during the contextmanager __exit__
            phase. Otherwise rows will be left in place. Defaults to True.
        """

        def sigil(v):
            if isinstance(v, self.Literal):
                return ":raw:"
            return ":"

        rows = list(rows)
        try:
            firstrow = rows[0]
        except IndexError:
            return
        columns = list(firstrow.keys())

        sql = f"""
            INSERT INTO {table} ({','.join(columns)})
            VALUES ({','.join(f'{sigil(firstrow[col])}{col}' for col in columns)})
        """
        if self.supports_returning:
            sql = sql + " RETURNING *"

        matching_rows_sql = f"""
            SELECT * FROM {table} WHERE
            {' OR '.join(
                f"({' AND '.join(f'{c}={sigil(row[c])}_{ix}_{c}' for c in row)})"
                for ix, row in enumerate(rows)
            )}
        """
        matching_row_count_sql = f"SELECT count(1) FROM ({matching_rows_sql}) as _"

        def get_matching_row_count():
            return Query(matching_row_count_sql).scalar(
                self.conn,
                **{
                    f"_{ix}_{k}": v
                    for ix, row in enumerate(rows)
                    for k, v in row.items()
                },
            )

        def get_matching_rows():
            return (
                Query(matching_rows_sql)
                .returning(dict)
                .many(
                    self.conn,
                    **{
                        f"_{ix}_{k}": v
                        for ix, row in enumerate(rows)
                        for k, v in row.items()
                    },
                )
            )

        if self.supports_returning:
            saved_row_count = None
            insert = Query(sql).returning(dict)
            result = [insert.one(self.conn, **row) for row in rows]
        else:
            saved_row_count = get_matching_row_count()
            if saved_row_count > 0:
                raise Exception(
                    f"Table already contains rows matching {rows}. Inserting more "
                    f"would make it impossible to remove the rows on exit"
                )
            insert = Query(sql)
            for row in rows:
                insert.execute(self.conn, **row)
            result = list(get_matching_rows())

        if commit:
            self.conn.commit()
        try:
            yield [AttrDict(r) for r in result]
        finally:
            if result and revert:
                if commit:
                    returned_columns = result[0]
                    where_clause = " AND ".join(f"{c} = :{c}" for c in returned_columns)
                    delete = Query(f"DELETE FROM {table} WHERE {where_clause}")
                    for row in result:
                        delete.execute(self.conn, **row)
                    self.conn.commit()
                else:
                    self.conn.rollback()
                    if (
                        not self.supports_returning
                        and saved_row_count != get_matching_row_count()
                    ):
                        raise AssertionError(
                            f"Fixture values committed by test code: "
                            f"expected {saved_row_count} rows but got "
                            f"{get_matching_row_count()}."
                        )

    @contextlib.contextmanager
    def update(
        self, table, values, where, commit=False, revert=False
    ) -> Generator["AttrDict", None, None]:
        """
        Update a single row to the specified values and yield an AttrDict of
        the updated row.

        On __exit__ revert to the previous values
        """
        where_clause = " AND ".join(
            f"({name}=:where_{name} OR ({name} IS NULL AND :where_{name} IS NULL))"
            for name in where
        )
        update_query = Query(
            f"""
            UPDATE {table} SET {', '.join(f'{name}=:value_{name}' for name in values)}
            WHERE {where_clause}
            """
        )
        select_updated_query = Query(f"SELECT * FROM {table} WHERE {where_clause}")
        save_query = Query(
            f"""
            SELECT {', '.join(values)}
            FROM {table}
            WHERE {where_clause}
            """
        )

        def get_save_values():
            saved_values = save_query.one_or_none(
                self.conn, **prefix_keys("where_", where)
            )
            if saved_values is not None:
                return dict(zip(values.keys(), saved_values))
            return None

        def _do_update(new_values, current_values={}):
            saved = get_save_values()
            assert saved is not None
            update_query.execute(
                self.conn,
                **merge(
                    prefix_keys("value_", new_values),
                    prefix_keys(
                        "where_",
                        merge(
                            where,
                            {k: v for k, v in current_values.items() if k in where},
                        ),
                    ),
                ),
            )
            updated_values = select_updated_query.returning(dict).one(
                self.conn,
                **prefix_keys(
                    "where_",
                    merge(
                        where,
                        {k: v for k, v in new_values.items() if k in where},
                    ),
                ),
            )
            return saved, AttrDict(updated_values)

        if commit:
            saved, updated = _do_update(values)
            try:
                self.conn.commit()
                yield updated
            finally:
                if revert:
                    new_values = get_save_values()
                    if saved != new_values:
                        raise AssertionError(
                            f"Cannot restore previous values: "
                            f"expected {saved!r} but got {new_values!r}."
                            f"Specify revert=False to disable this check"
                        )
                    _do_update(saved, values)
                self.conn.commit()

        elif revert:
            with savepoint(self.conn):
                saved, updated = _do_update(values)
                yield updated
        else:
            saved, updated = _do_update(values)
            yield updated


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


def merge(*ds):
    result = {}
    for d in ds:
        result.update(d)
    return result


def prefix_keys(prefix, d):
    return {f"{prefix}{k}": v for k, v in d.items()}


@contextlib.contextmanager
def savepoint(conn):
    savepoint_name = "_" + str(uuid1()).replace("-", "_")
    cursor = conn.cursor()
    cursor.execute("SAVEPOINT " + savepoint_name)
    try:
        yield savepoint_name
    finally:
        cursor.execute(f"ROLLBACK TO {savepoint_name}")
