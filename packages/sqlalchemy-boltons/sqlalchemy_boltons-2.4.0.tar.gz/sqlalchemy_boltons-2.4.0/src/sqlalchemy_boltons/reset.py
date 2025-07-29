from __future__ import annotations

import typing as ty

import sqlalchemy as sa

try:
    from sqlalchemy.events import PoolResetState
except ImportError:
    PoolResetState = None

# public API
__all__ = ["install_reset_auto", "UnsupportedDialectError"]


dialect_to_install_reset: dict[str, ty.Callable[[sa.Engine], None]] = {}


def register_resetter(name):
    def decorator(func):
        dialect_to_install_reset[name] = func
        return func

    return decorator


class UnsupportedDialectError(ValueError):
    pass


def install_reset_auto(engine: sa.Engine) -> None:
    """
    Install the reset event handler for *engine*. This function automatically detects the right resetter to install,
    and raises an exception if the SQL dialect is not supported.

    **Important**: You should disable the default reset handler (which just does a rollback) using
    ``create_engine(..., pool_reset_on_return=False)``.
    """
    name = engine.dialect.name
    try:
        func = dialect_to_install_reset[name]
    except KeyError:
        raise UnsupportedDialectError("Unsupported dialect {name!r}.")
    func(engine)


@register_resetter("sqlite")
@register_resetter("mysql")
@register_resetter("mariadb")
@register_resetter("oracle")
def install_reset_generic(engine: sa.Engine):
    """Default resetter which only does a rollback."""

    @sa.event.listens_for(engine, "reset")
    def reset_generic(dbapi_connection, connection_record, reset_state):
        dbapi_connection.rollback()


@register_resetter("postgresql")
def install_reset_postgresql(engine: sa.Engine):
    """
    Postgresql requires additional commands to end all transactions in progress and discard temporary tables.

    References:

    - https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#temporary-table-resource-reset-for-connection-pooling
    """

    @sa.event.listens_for(engine, "reset")
    def _reset_postgresql(dbapi_connection, connection_record, reset_state):
        if is_safe_to_execute_sql(dbapi_connection, connection_record, reset_state):
            dbapi_connection.execute("CLOSE ALL")
            dbapi_connection.execute("RESET ALL")
            dbapi_connection.execute("DISCARD TEMP")

        # so that the DBAPI itself knows that the connection has been
        # reset
        dbapi_connection.rollback()


@register_resetter("mssql")
def install_reset_mssql(engine: sa.Engine):
    """
    This calls a semi-documented stored procedure called "sys.sp_reset_connection" which does lots of cleanup actions.

    References:

    - https://docs.sqlalchemy.org/en/20/dialects/mssql.html#temporary-table-resource-reset-for-connection-pooling
    - https://github.com/sqlalchemy/sqlalchemy/issues/8693
    """

    @sa.event.listens_for(engine, "reset")
    def _reset_mssql(dbapi_connection, connection_record, reset_state):
        if is_safe_to_execute_sql(dbapi_connection, connection_record, reset_state):
            dbapi_connection.execute("{call sys.sp_reset_connection}")

        # So that the DBAPI itself knows that the connection has been
        # reset
        dbapi_connection.rollback()


if PoolResetState is None:  # SQLAlchemy 1.4

    def is_safe_to_execute_sql(dbapi_connection, connection_record, reset_state):
        return True

else:  # SQLAlchemy 2.0

    def is_safe_to_execute_sql(dbapi_connection, connection_record, reset_state):
        return not reset_state.terminate_only
