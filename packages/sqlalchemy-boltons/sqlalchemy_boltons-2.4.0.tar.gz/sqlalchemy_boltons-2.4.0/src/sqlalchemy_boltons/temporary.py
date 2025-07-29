from __future__ import annotations

import contextlib
import dataclasses
import functools
import logging
import os
import typing as ty

import sqlalchemy as sa
from sqlalchemy import orm as sao

__all__ = ["temporary_table", "UnsupportedDialectError"]

logger = logging.getLogger(__name__)


class UnsupportedDialectError(ValueError):
    pass


_Mapped = ty.Any


def temporary_table(
    bind: sa.Connection | sao.Session,
    table: sa.Table | _Mapped,
    *,
    require_dialect_support: bool = True,
    metadata=None,
    name_prefix: str = "_tmp_",
    name_suffix: str = None,
):
    """
    This context manager creates a temporary table which is valid within the current "with" block.
    The temporary table is dropped as soon as the "with" block completes, or at the end of the transaction if the
    dialect supports it.

    By default, this function creates the table in a brand new :class:`sqlalchemy.MetaData`. If you want to create the
    table inside an existing one, then pass in the *metadata* argument.

    If you want something that persists past the end of the transaction, then you probably want an actual persistent
    table. If you think about it some more, you will realize that you probably also want some way to keep track of these
    semi-persistent tables, and automatically discard them if they are too old. We will someday provide a way to do that
    too, maybe.

    Tested on SQLite, Postgres, and MariaDB/MySQL.

    Based on https://github.com/sqlalchemy/sqlalchemy/discussions/9400
    """

    if isinstance(bind, sao.Session):
        session = bind
        bind = None
    else:
        session = None

    return TemporaryTableBuilder(
        bind=bind,
        session=session,
        table_to_copy=table,
        metadata=metadata,
        require_dialect_support=require_dialect_support,
        name_prefix=name_prefix,
        name_suffix=name_suffix,
    ).context()


@contextlib.contextmanager
def context_create_and_drop(bind: sa.Connection, t: sa.Table):
    t.create(bind)
    try:
        yield t
    finally:
        try:
            t.drop(bind, checkfirst=True)
        except Exception:
            logger.warning(f"error while dropping table {t.name}", exc_info=True)


@dataclasses.dataclass(eq=False)
class TemporaryTableBuilder:
    session: sao.Session | None
    bind: sa.Connection | None
    table_to_copy: sa.Table | _Mapped
    metadata: sa.MetaData | None
    require_dialect_support: bool
    name_prefix: str
    name_suffix: str | None

    def __post_init__(self):
        self._resolve_arguments()

    def _resolve_arguments(self):
        if not isinstance(self.table_to_copy, sa.Table):
            self.table_to_copy = sa.inspect(self.table_to_copy).local_table

        if self.metadata is None:
            self.metadata = sa.MetaData()

        if self.bind is None:
            self.bind = self.session.connection(bind_arguments=dict(clause=sa.select(self.table_to_copy)))

        if self.name_suffix is None:
            # default name to the table we're copying from
            self.name_suffix = "_" + self.table_to_copy.name

    @classmethod
    def _set_table_prefix_temporary(cls, table: sa.Table):
        table._prefixes = ["TEMPORARY"]

    @classmethod
    def configure_temporary_table_mariadb(cls, table: sa.Table):
        cls._set_table_prefix_temporary(table)

    @classmethod
    def configure_temporary_table_mysql(cls, table: sa.Table):
        cls._set_table_prefix_temporary(table)

    @classmethod
    def configure_temporary_table_postgresql(cls, table: sa.Table):
        cls._set_table_prefix_temporary(table)
        table.dialect_kwargs["postgresql_on_commit"] = "DROP"

    @classmethod
    def configure_temporary_table_sqlite(cls, table: sa.Table):
        cls._set_table_prefix_temporary(table)

    def _get_dialect_name(self):
        return self.bind.dialect.name

    def _make_configure_temporary_table_method_name(self, s):
        return _make_configure_temporary_table_method_name(s)

    def _generate_table_name(self) -> str:
        inspector = sa.inspect(self.bind)
        for nbytes in range(2, 21):
            hexstr = os.urandom(nbytes).hex()
            name = f"{self.name_prefix}{hexstr}{self.name_suffix}"
            if not inspector.has_table(name):
                return name
        else:
            raise AssertionError("could not find unused table name, do you really have 2**160 temporary tables?")

    def make_table(self, name: str = None) -> sa.Table:
        name = name or self._generate_table_name()
        t = self.table_to_copy.to_metadata(self.metadata, name=name)
        configure = getattr(self, self._make_configure_temporary_table_method_name(self._get_dialect_name()), None)
        if configure is None:
            if self.require_dialect_support:
                raise UnsupportedDialectError(
                    "SQL dialect not supported, either implement it or use require_dialect_support=False"
                )
        else:
            configure(t)

        if self.session is not None:
            self.session.bind_table(t, self.bind)

        return t

    @contextlib.contextmanager
    def context(self):
        t = self.make_table()
        with context_create_and_drop(self.bind, t):
            yield t


@functools.cache
def _make_configure_temporary_table_method_name(s):
    return f"configure_temporary_table_{s}"
