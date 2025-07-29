import contextlib
import os

import pytest
import sqlalchemy as sa
import sqlalchemy.orm as sao

from sqlalchemy_boltons import sqlite as _sq


# change this if every this situation changes https://sqlite.org/forum/info/6700ab1f9f6e8a00
HAS_MEMDB_MVCC = False

Base = sao.declarative_base()


class Example(Base):
    __tablename__ = "ex1"

    id = sa.Column(sa.Integer, primary_key=True)


class Example2(Base):
    __tablename__ = "ex2"

    id = sa.Column(sa.ForeignKey("ex1.id"), primary_key=True)


@contextlib.contextmanager
def temporary_chdir(path):
    old = os.getcwd()
    try:
        os.chdir(str(path))
        yield
    finally:
        os.chdir(old)


def test_invalid():
    with pytest.raises(ValueError):
        _sq.make_journal_mode_statement("!@#$")
    with pytest.raises(ValueError):
        _sq.make_begin_statement("!@#$")
    with pytest.raises(ValueError):
        _sq.make_foreign_keys_settings("!@#$")


@pytest.fixture(scope="function")
def simple_sqlite_engine(tmp_path, database_type):
    if database_type == "file":
        path = tmp_path / "x.db"
    elif database_type == "memory":
        path = _sq.Memory()
    else:
        raise AssertionError

    return _sq.create_engine_sqlite(
        path, journal_mode="WAL", timeout=0.5, create_engine_args={"echo": True, "pool_timeout": 2}
    )


@pytest.mark.parametrize("database_type", ["file", "memory"])
def test_transaction(simple_sqlite_engine, database_type):
    has_mvcc: bool = (database_type != "memory") or HAS_MEMDB_MVCC

    engine = simple_sqlite_engine
    engine = engine.execution_options(x_sqlite_foreign_keys="defer")

    with pytest.raises(Exception, match="You must configure your engine"):
        with engine.begin():
            pass

    engine_r = engine.execution_options(x_sqlite_begin_mode=None)
    engine_w = engine.execution_options(x_sqlite_begin_mode="IMMEDIATE")

    SessionR = sao.sessionmaker(engine_r)
    SessionW = sao.sessionmaker(engine_w)

    if has_mvcc:
        with engine_r.begin() as conn:
            actual_journal_mode = _sq.sqlite_journal_mode(conn)
        assert actual_journal_mode.upper() == "WAL"

    # read transactions can be concurrent
    with engine_r.begin() as s:
        with engine_r.begin() as s2:
            pass

    # write transactions cannot
    with engine_w.begin() as s:
        with pytest.raises(sa.exc.OperationalError):
            with engine_w.begin() as s2:
                pass

    # create schema
    with SessionW() as s:
        Base.metadata.create_all(s.connection())
        s.add(Example(id=1))
        s.flush()
        s.commit()

    # test basic ACID assumptions
    with SessionW() as s:
        s.add(Example(id=2))
        s.flush()

        assert len(s.execute(sa.select(Example)).all()) == 2

        if has_mvcc:
            # concurrent connections not supported for memdb yet :(
            with SessionR() as s2:
                assert len(s2.execute(sa.select(Example)).all()) == 1

        with pytest.raises(sa.exc.OperationalError):
            with SessionW() as s2:
                s2.add(Example(id=2))
                s2.flush()

        assert len(s.execute(sa.select(Example)).all()) == 2
        s.commit()

    with contextlib.ExitStack() as exit_stack:
        # concurrent connection count
        for i in range(30):
            exit_stack.enter_context(s := SessionR())
            assert len(s.execute(sa.select(Example)).all()) == 2


@pytest.mark.parametrize("path_type", ["str", "Path"])
def test_create_engine_path(tmp_path, path_type):
    path = tmp_path / "x.db"

    if path_type == "str":
        path_ = str(path)
    else:
        path_ = path

    assert not path.exists()

    engine = _sq.create_engine_sqlite(path_, journal_mode="WAL", timeout=0.5, create_engine_args={"echo": True})
    engine = engine.execution_options(x_sqlite_begin_mode=None, x_sqlite_foreign_keys="defer")

    with sao.Session(bind=engine) as s:
        Base.metadata.create_all(s.connection())
        s.commit()

    assert path.exists()


def test_relative_path(tmp_path):
    name = "relative.db"
    path = tmp_path / name
    assert not path.exists()

    with temporary_chdir(tmp_path):
        engine = _sq.create_engine_sqlite(name, journal_mode="WAL", timeout=0.5)

    engine = engine.execution_options(x_sqlite_begin_mode="IMMEDIATE", x_sqlite_foreign_keys="defer")
    with engine.begin():
        pass

    assert path.exists()


def _test_fk_common(engine, foreign_keys):
    engine = engine.execution_options(x_sqlite_begin_mode="IMMEDIATE", x_sqlite_foreign_keys=foreign_keys)

    with sao.Session(bind=engine) as s:
        Base.metadata.create_all(s.connection())
        s.add(Example(id=1))
        s.commit()

    return engine


@pytest.mark.parametrize("database_type", ["file", "memory"])
def test_fk_off(simple_sqlite_engine):
    engine = _test_fk_common(simple_sqlite_engine, False)

    with sao.Session(bind=engine) as s:
        s.add(Example2(id=2))
        s.flush()
        s.commit()


@pytest.mark.parametrize("database_type", ["file", "memory"])
def test_fk_defer(simple_sqlite_engine):
    engine = _test_fk_common(simple_sqlite_engine, "defer")

    with sao.Session(bind=engine) as s:
        s.add(Example2(id=2))
        s.flush()
        with pytest.raises(sa.exc.IntegrityError):
            s.commit()


@pytest.mark.parametrize("database_type", ["file", "memory"])
def test_fk_on(simple_sqlite_engine):
    engine = _test_fk_common(simple_sqlite_engine, True)

    with sao.Session(bind=engine) as s:
        with pytest.raises(sa.exc.IntegrityError):
            s.add(Example2(id=2))
            s.flush()
