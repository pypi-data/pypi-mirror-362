from __future__ import annotations

import dataclasses as dc
import functools
from pathlib import Path
import typing as ty
from urllib import parse as _up

import sqlalchemy as sa
from sqlalchemy import pool as sap

__all__ = [
    "create_engine_sqlite",
    "SQLAlchemySqliteTransactionFix",
    "sqlite_file_uri",
    "sqlite_journal_mode",
    "MissingExecutionOptionError",
]


class MissingExecutionOptionError(ValueError):
    pass


@functools.lru_cache(maxsize=64)
def make_journal_mode_statement(mode: str | None) -> str:
    if mode:
        if not mode.isalnum():
            raise ValueError(f"invalid mode {mode!r}")
        return f"PRAGMA journal_mode={mode}"
    else:
        return "PRAGMA journal_mode"


@functools.lru_cache(maxsize=64)
def make_begin_statement(mode: str | None) -> str:
    if mode and not mode.isalpha():
        raise ValueError(f"invalid mode {mode!r}")
    return f"BEGIN {mode}" if mode else "BEGIN"


@functools.lru_cache(maxsize=64)
def make_foreign_keys_settings(foreign_keys: bool | str) -> tuple[str, str | None]:
    if foreign_keys is True:
        return "PRAGMA foreign_keys=1", None
    elif foreign_keys is False:
        return "PRAGMA foreign_keys=0", None
    elif foreign_keys == "defer":
        return "PRAGMA foreign_keys=1", "PRAGMA defer_foreign_keys=1"
    else:
        raise ValueError("invalid value {foreign_keys!r} for x_sqlite_foreign_keys")


class SQLAlchemySqliteTransactionFix:
    """
    This class exists because sqlalchemy doesn't automatically fix pysqlite's stupid default behaviour. Additionally,
    we implement support for foreign keys.

    The execution options we look for are as follows:

    - `x_sqlite_begin_mode`: The type of transaction to be started, such as "BEGIN" or
      "[BEGIN IMMEDIATE](https://www.sqlite.org/lang_transaction.html)" (or
      "[BEGIN CONCURRENT](https://www.sqlite.org/cgi/src/doc/begin-concurrent/doc/begin_concurrent.md)" someday maybe).
    - `x_sqlite_foreign_keys`: The [foreign-key enforcement setting](https://www.sqlite.org/foreignkeys.html). Must be
      `True`, `False`, or `"defer"`.
    - `x_sqlite_journal_mode`: The [journal mode](https://www.sqlite.org/pragma.html#pragma_journal_mode) such as
      `"DELETE"` or `"WAL"`. Optional.

    https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#serializable-isolation-savepoints-transactional-ddl
    """

    def register(self, engine):
        sa.event.listen(engine, "connect", self.event_connect)
        sa.event.listen(engine, "begin", self.event_begin)

    def make_journal_mode_statement(self, mode: str | None):
        return make_journal_mode_statement(mode)

    def make_begin_statement(self, mode: str | None):
        return make_begin_statement(mode)

    def make_foreign_keys_settings(self, foreign_keys: bool | str) -> tuple[str, str | None]:
        return make_foreign_keys_settings(foreign_keys)

    def event_connect(self, dbapi_connection, connection_record):
        # disable pysqlite's emitting of the BEGIN statement entirely.
        # also stops it from emitting COMMIT before any DDL.
        dbapi_connection.isolation_level = None

    def event_begin(self, conn):
        execution_options = conn.get_execution_options()

        try:
            opt_begin = execution_options["x_sqlite_begin_mode"]
            opt_fk = execution_options["x_sqlite_foreign_keys"]
        except KeyError as exc:
            raise MissingExecutionOptionError(
                "You must configure your engine (or connection) execution options. "
                "For example:\n\n"
                "    engine = create_engine_sqlite(...)\n"
                '    engine = engine.execution_options(x_sqlite_foreign_keys="defer")\n'
                "    engine_ro = engine.execution_options(x_sqlite_begin_mode=None)\n"
                '    engine_rw = engine.execution_options(x_sqlite_begin_mode="IMMEDIATE")'
            ) from exc
        begin = self.make_begin_statement(opt_begin)
        before, after = self.make_foreign_keys_settings(opt_fk)

        if mode := execution_options.get("x_sqlite_journal_mode"):
            conn.exec_driver_sql(self.make_journal_mode_statement(mode)).close()

        conn.exec_driver_sql(before).close()
        conn.exec_driver_sql(begin).close()
        if after:
            conn.exec_driver_sql(after).close()


@dc.dataclass
class Memory:
    """
    We keep a reference to an open connection because SQLite will free up the database otherwise.

    Note that you still can't get concurrent readers and writers because you cannot currently set WAL mode on an
    in-memory database. See https://sqlite.org/forum/info/6700ab1f9f6e8a00
    """

    uri: str = dc.field(init=False)
    connection_reference = None

    def __post_init__(self):
        self.uri = f"file:/sqlalchemy_boltons_memdb_{id(self)}"

    def as_uri(self):
        return self.uri


def sqlite_file_uri(path: Path | str | Memory, parameters: ty.Sequence[tuple[str | bytes, str | bytes]] = ()) -> str:
    if isinstance(path, str):
        path = Path(path)
    if isinstance(path, Path) and not path.is_absolute():
        path = path.absolute()

    qs = _up.urlencode(parameters, quote_via=_up.quote)
    qm = "?" if qs else ""
    return f"{path.as_uri()}{qm}{qs}"


def sqlite_journal_mode(connection, mode: str | None = None) -> str:
    [[value]] = connection.exec_driver_sql(make_journal_mode_statement(mode))
    return value


def create_engine_sqlite(
    path: Path | str | Memory,
    *,
    timeout: float | int | None,
    parameters: ty.Iterable[tuple[str | bytes, str | bytes]] = (),
    journal_mode: str | None = None,
    check_same_thread: bool | None = False,
    create_engine_args: dict | None = None,
    create_engine: ty.Callable | None = None,
    transaction_fix: SQLAlchemySqliteTransactionFix | bool = True,
) -> sa.Engine:
    """
    Create a sqlite engine.

    Parameters
    ----------
    path: Path | str | Memory
        Path to the db file, or a :class:`Memory` object. The same memory object can be shared across multiple engines.
    timeout: float
        How long will SQLite wait if the database is locked? See
        https://docs.python.org/3/library/sqlite3.html#sqlite3.connect
    parameters: ty.Sequence, optional
        SQLite URI query parameters as described in https://www.sqlite.org/uri.html
    journal_mode: str, optional
        If provided, set the journal mode to this string before every transaction. This option simply sets the
        ``x_sqlite_journal_mode`` engine execution option.
    check_same_thread: bool, optional
        Defaults to False. See https://docs.python.org/3/library/sqlite3.html#sqlite3.connect
    create_engine_args: dict, optional
        Keyword arguments to be passed to :func:`sa.create_engine`.
    create_engine: callable, optional
        If provided, this will be used instead of :func:`sa.create_engine`. You can use this to further customize
        the engine creation.
    transaction_fix: SQLAlchemySqliteTransactionFix | bool, optional
        See :class:`SQLAlchemySqliteTransactionFix`. If True, then instantiate one. If False, then do not apply the fix.
        (default: True)
    """

    parameters = list(parameters)
    if isinstance(path, Memory):
        parameters += (("vfs", "memdb"),)
    parameters.append(("uri", "true"))

    uri = sqlite_file_uri(path, parameters)

    if create_engine_args is None:
        create_engine_args = {}  # pragma: no cover

    # always default to QueuePool
    if (k := "poolclass") not in create_engine_args:
        create_engine_args[k] = sap.QueuePool
        if (k := "max_overflow") not in create_engine_args:
            # for SQLite it doesn't make sense to restrict the number of concurrent (read-only) connections
            create_engine_args["max_overflow"] = -1

    if (v := create_engine_args.get(k := "connect_args")) is None:
        create_engine_args[k] = v = {}
    if timeout is not None:
        v["timeout"] = timeout
    if check_same_thread is not None:
        v["check_same_thread"] = check_same_thread

    # do not pass through poolclass=None
    if create_engine_args.get((k := "poolclass"), True) is None:
        create_engine_args.pop(k, None)  # pragma: no cover

    if create_engine is None:
        create_engine = sa.create_engine

    engine = create_engine("sqlite:///" + uri, **create_engine_args)

    if transaction_fix is True:
        transaction_fix = SQLAlchemySqliteTransactionFix()

    if transaction_fix:
        transaction_fix.register(engine)

    engine = engine.execution_options(x_sqlite_journal_mode=journal_mode)

    if isinstance(path, Memory):
        (conn := engine.raw_connection()).detach()

        # force the connection to actually happen
        conn.execute("SELECT 0 WHERE 0").close()

        path.connection_reference = conn

    return engine
