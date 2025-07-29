import pytest
from pifpaf.drivers.postgresql import PostgreSQLDriver
from pifpaf.drivers.mysql import MySQLDriver
import sqlalchemy as sa
from sqlalchemy import orm as sao, exc as sa_exc

from sqlalchemy_boltons.core import count1
from sqlalchemy_boltons.sqlite import create_engine_sqlite
from sqlalchemy_boltons.temporary import temporary_table, TemporaryTableBuilder


def _pifpaf_fixture(driver, force_uri_scheme: str = None, create_engine_kw: dict = None):
    if create_engine_kw is None:
        create_engine_kw = {}
    driver.setUp()
    try:
        uri = driver.env["PIFPAF_URL"]
        if force_uri_scheme:
            before, sep, after = uri.partition(":")
            uri = sep.join((force_uri_scheme, after))
        engine = sa.create_engine(uri, **create_engine_kw)
        yield engine
    finally:
        driver.cleanUp()


@pytest.fixture(scope="module")
def pifpaf_postgresql():
    yield from _pifpaf_fixture(PostgreSQLDriver(), create_engine_kw=dict(echo=True))


@pytest.fixture(scope="module")
def pifpaf_mysql():
    yield from _pifpaf_fixture(MySQLDriver(), create_engine_kw=dict(echo=True))


@pytest.fixture(scope="function")
def sa_engine_sqlite(tmp_path):
    engine = create_engine_sqlite(
        tmp_path / "sa_engine_sqlite.db",
        journal_mode="WAL",
        timeout=0.5,
        create_engine_args=dict(echo=True, pool_timeout=2),
    ).execution_options(x_sqlite_foreign_keys="defer", x_sqlite_begin_mode=None)
    yield engine


@pytest.fixture
def sa_engine(request):
    return request.getfixturevalue(request.param)


Base = sao.declarative_base()


class Cake(Base):
    __tablename__ = "orm_cake"

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column("name", sa.String(32), unique=True)


_CAKES = [
    {"id": 3, "name": "red velvet"},
    {"id": 4, "name": "chocolate mousse"},
    {"id": 6, "name": "black forest"},
    {"id": 7, "name": "tiramisu"},
]


table_def = sa.Table(
    "core_cake",
    sa.MetaData(),
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("name", sa.String(32), unique=True),
)


@pytest.mark.parametrize("sa_engine", ["sa_engine_sqlite", "pifpaf_postgresql"], indirect=True)
def test_temporary_example(sa_engine):
    Session = sao.sessionmaker(sa_engine)

    tmp_table_def = sa.Table(
        "ids",
        sa.MetaData(),
        sa.Column("id", sa.Integer, primary_key=True),
    )

    my_ids = [1, 23, 4, 5, 67, 89]

    with Session() as s:
        Base.metadata.create_all(s.connection())
        s.execute(sa.insert(Cake), _CAKES)

        with temporary_table(s, tmp_table_def) as tmp:
            s.execute(sa.insert(tmp), [{"id": x} for x in my_ids]).close()
            results = s.execute(sa.select(Cake).join(tmp, tmp.c.id == Cake.id)).scalars().all()

            assert len(results) == 1
            assert results[0].id == 4


@pytest.mark.parametrize("table_type", ["table", "mapper", "mapped_class"])
@pytest.mark.parametrize("sa_engine", ["sa_engine_sqlite", "pifpaf_mysql", "pifpaf_postgresql"], indirect=True)
def test_temporary_table(sa_engine, table_type):
    if table_type == "table":
        table_to_copy = table_def
    elif table_type == "mapped_class":
        table_to_copy = Cake
    elif table_type == "mapper":
        table_to_copy = sa.inspect(Cake)
    else:
        raise AssertionError

    if sa_engine.dialect.name == "sqlite":
        missing_exc = sa_exc.OperationalError
    else:
        missing_exc = sa_exc.ProgrammingError

    Session = sao.sessionmaker(sa_engine)

    with Session() as s:
        if sa_engine.dialect.name == "mysql":
            # FIXME: WHY IS THIS NEEDED?? This block never commits, so how is the table still there?
            Base.metadata.drop_all(s.connection())
        Base.metadata.create_all(s.connection())

        with temporary_table(s, table_to_copy) as t:
            s.execute(sa.insert(t), _CAKES)

            with pytest.raises(sa_exc.IntegrityError), s.begin_nested():
                # PK collision
                s.execute(sa.insert(t), [{"id": 3, "name": "rum"}])

            with pytest.raises(sa_exc.IntegrityError), s.begin_nested():
                # unique constraint violation
                s.execute(sa.insert(t), [{"id": 999, "name": "chocolate mousse"}])

            assert s.execute(sa.select(count1()).select_from(t)).scalar() == len(_CAKES)

            s.execute(sa.insert(Cake).from_select(["name", "id"], sa.select(t.c.name, t.c.id).where(t.c.id != 4)))

        with pytest.raises(missing_exc), s.begin_nested():
            s.execute(sa.select(count1()).select_from(t))

        assert s.execute(sa.select(count1()).select_from(Cake)).scalar() == len(_CAKES) - 1

        s.rollback()

    with Session() as s:
        t = TemporaryTableBuilder(
            session=s,
            bind=None,
            table_to_copy=table_to_copy,
            metadata=sa.MetaData(),
            require_dialect_support=True,
            name_prefix=None,
            name_suffix=None,
        ).make_table("pie")
        t.create(s.connection())
        assert sa.inspect(s.connection()).has_table("pie")
        s.commit()

    try:
        if sa_engine.dialect.name != "postgresql":
            # SQLite TEMP tables stick around for the duration of the session if you commit them.
            # The same holds true for MariaDB. To avoid this issue, we close all connections to prevent reuse.
            sa_engine.dispose()

        with Session() as s:
            assert not sa.inspect(s.connection()).has_table("pie")
    finally:
        with Session() as s:
            t.drop(s.connection(), checkfirst=True)
            s.commit()
