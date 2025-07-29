import sqlite3
from unittest.mock import Mock
from unittest.mock import call
from unittest.mock import mock_open
from sqlfixtures.sqlfixture import SQLFixture
from sqlfixtures.insertable import Insertable
from sqlfixtures.insertable import Reference
from sqlfixtures.insertable import SELF
from sqlfixtures.insertable import apply_to_fixture

import pytest


@pytest.fixture()
def sqlite_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE foo (x varchar(10), y int)")
    yield conn
    conn.close()


@pytest.fixture()
def fixture(sqlite_db):
    yield SQLFixture(sqlite_db)


def test_insertable_constructor():

    i = Insertable("foo", x="1", y=2)
    assert i.table == "foo"
    assert Insertable.as_dict(i) == {"x": "1", "y": 2}


def test_it_applies_to_fixture(sqlite_db):
    fixture = SQLFixture(sqlite_db)
    to_insert = {"foo": Insertable("foo", x="1", y=2)}
    with apply_to_fixture(fixture, to_insert) as data:
        cursor = sqlite_db.cursor()
        cursor.execute("SELECT * FROM foo")
        assert cursor.fetchall() == [("1", 2)]


def test_it_creates_a_copy_on_call():
    i = Insertable("foo", {"x": 1})
    j = i()
    assert j.table == "foo"
    assert j._items == {"x": 1}


def test_it_allows_table_override_on_call():
    i = Insertable("foo", {"x": 1})
    j = i("bar")
    assert j.table == "bar"
    assert j._items == {"x": 1}


def test_it_allows_item_override_on_call():
    i = Insertable("foo", {"x": 1})
    j = i(x=2, y=3)
    assert j.table == "foo"
    assert j._items == {"x": 2, "y": 3}


def test_it_allows_or():
    i = Insertable("foo", {"x": 1})
    j = i | {"y": 2}
    assert j.table == "foo"
    assert j._items == {"x": 1, "y": 2}


def test_it_creates_a_self_reference(fixture):
    i = Insertable("foo", x=1, y=SELF.x)
    with apply_to_fixture(fixture, {"i": i}) as data:
        assert data["i"]["x"] == "1"
        assert data["i"]["y"] == 1


def test_it_creates_a_self_reference_in__call__(fixture):
    i = Insertable("foo", y=SELF.x)
    j = i(x=1)
    with apply_to_fixture(fixture, {"j": j}) as data:
        assert data["j"]["x"] == "1"
        assert data["j"]["y"] == 1


def test_it_can_reference_parent(fixture):
    foo = Insertable(
        "foo",
        x="parent",
        y=2,
        child=Insertable("foo", x="child", y=SELF._parent.y)
    )
    with apply_to_fixture(fixture, {"foo": foo}) as data:
        assert data.foo.child.y == 2  # type: ignore


def test_it_does_late_update(fixture):
    foo = Insertable(
        "foo",
        x="parent",
        y=2,
        child=Insertable("foo", x="child", y=0).after(y=SELF._parent.y)
    )
    with apply_to_fixture(fixture, {"foo": foo}) as data:
        assert data.foo.child.y == 2  # type: ignore


def test_it_unpeels_reference():
    foo = Insertable("foo", x=1, y=Insertable("bar"))
    ref = foo.y.z
    newref, remaining = ref.unpeel()
    assert newref.source is foo.y
    assert remaining is None


def test_insertables_are_isolated():
    foo = Insertable("foo", x=1)
    bar = foo(x=2, y=1)
    assert foo._items == {"x": 1}


def test_after_is_called(fixture):
    foo = Insertable("foo", x=1).after(x=2)
    with apply_to_fixture(fixture, {"foo": foo}) as data:
        assert data.foo.x == 2
