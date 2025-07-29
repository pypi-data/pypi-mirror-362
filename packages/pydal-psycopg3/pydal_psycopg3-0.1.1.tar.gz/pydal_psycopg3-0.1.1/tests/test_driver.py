import tempfile
from contextlib import chdir

import pytest
from pydal import DAL
from testcontainers.postgres import PostgresContainer

postgres = PostgresContainer(
    dbname="postgres",
    username="someuser",
    password="somepass",
)


@pytest.fixture(scope="module", autouse=True)
def psql(request):
    postgres.ports = {
        5432: 9631,  # as set in valid.env
    }

    request.addfinalizer(postgres.stop)
    postgres.start()


@pytest.fixture
def at_temp_dir():
    with tempfile.TemporaryDirectory() as d:
        with chdir(d):
            yield d


def test_no_driver(at_temp_dir):
    with pytest.raises(RuntimeError):
        db = DAL("postgres://someuser:somepass@localhost:9631/postgres")


def test_db_original_scheme(at_temp_dir):
    from src import pydal_psycopg3

    print("using", pydal_psycopg3, "driver")

    db = DAL("postgres://someuser:somepass@localhost:9631/postgres")

    table = db.define_table("test_table_one", db.Field("test_field"))
    db.commit()

    assert table.insert(test_field="one")

    assert db.executesql("""
    select * from test_table_one
    """)

    db.commit()

    db(table).delete()
    db.rollback()

    assert db.executesql("""
    select * from test_table_one
    """)

    db(table).delete()
    db.commit()

    assert not db.executesql("""
    select * from test_table_one
    """)


def test_db_custom_scheme(at_temp_dir):
    from src import pydal_psycopg3

    print("using", pydal_psycopg3, "driver")

    db = DAL("postgres:psycopg3://someuser:somepass@localhost:9631/postgres")

    table = db.define_table("test_table_two", db.Field("test_field"))
    db.commit()

    assert table.insert(test_field="one")

    assert db.executesql("""
    select * from test_table_two
    """)

    db.commit()

    db(table).delete()
    db.rollback()

    assert db.executesql("""
    select * from test_table_two
    """)

    db(table).delete()
    db.commit()

    assert not db.executesql("""
    select * from test_table_two
    """)
