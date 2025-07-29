from __future__ import annotations

import dataclasses
import functools
import typing as ty

from sqlalchemy.exc import NoResultFound
import sqlalchemy.orm as _sao
from sqlalchemy.orm.util import identity_key
from sqlalchemy.sql import coercions as _coercions, util as _util, ColumnCollection

__all__ = ["RelationshipComparator", "join_expr", "Relationships", "IdKey"]


class RelationshipComparator:
    """
    This wrapper makes it possible to compare a table against a relationship using :func:`join_expr`. This can be used
    for constructing a subquery that filters using a relationship to a table from the outer query.

    For example::

        import sqlalchemy as sa
        from sqlalchemy import orm as sao
        from sqlalchemy_boltons.orm import RelationshipComparator as Rel

        Base = sao.declarative_base()


        class Parent(Base):
            __tablename__ = "parent"

            id = sa.Column(sa.Integer, primary_key=True)

            children = sao.relationship("Child", back_populates="parent")


        class Child(Base):
            __tablename__ = "child"

            id = sa.Column(sa.Integer, primary_key=True)
            parent_id = sa.Column(sa.ForeignKey("parent.id"), index=True)

            parent = sao.relationship("Parent", back_populates="children")


        # We want a query that selects every Parent that has at least one child. We also want to use aliases.
        P = sao.aliased(Parent)
        C = sao.aliased(Child)

        # This is the boring old way of doing it, which requires explicitly stating the filtering conditions in terms
        # of the columns in both tables.
        q1 = sa.select(P).where(sa.select(C).where(C.parent_id == P.id).exists())

        # Reuse the filtering conditions from the ORM relationship!
        q2 = sa.select(P).where(sa.select(C).where(Rel(C.parent) == P).exists())

        assert str(q1) == str(q2), "these should produce the same SQL code!"

    Based on this discussion: https://groups.google.com/g/sqlalchemy/c/R-qOlzzVi0o/m/NtFswgJioDIJ
    """

    def __init__(self, relationship):
        self._relationship = relationship

    def __eq__(self, other):
        if other is None:
            raise TypeError("cannot compare against None")
        return join_expr(other, self._relationship)

    def __ne__(self, other):
        return ~(self == other)


def join_expr(right, relationship):
    """
    Turn an ORM relationship into an expression that you can use for filtering.
    """

    expr = _coercions.expect(_coercions.roles.ColumnArgumentRole, relationship)
    if right is not None:
        right = _coercions.expect(_coercions.roles.FromClauseRole, right)
        expr = _util.ClauseAdapter(right).traverse(expr)
    return expr


T = ty.TypeVar("T")


@dataclasses.dataclass(frozen=True)
class IdKey(ty.Generic[T]):
    """
    Holds the primary key information for an ORM instance. This is useful for passing a reference
    to an ORM object across different sessions and/or threads.

    For example::

        import sqlalchemy as sa
        from sqlalchemy import orm as sao
        from sqlalchemy_boltons.orm import IdKey

        Base = sao.declarative_base()


        class MyClass(Base):
            __tablename__ = "my_table"

            id = sa.Column(sa.Integer, primary_key=True)


        session = Session()
        instance = session.execute(sa.select(MyClass).where(...)).one()
        key = IdKey.from_instance(instance)

        # ...later...
        session = Session()
        instance = key.get_one(session)
    """

    mapped: type[T]
    key: tuple
    identity_token: ty.Any

    @classmethod
    def from_instance(cls, instance: T) -> IdKey[T]:
        if isinstance(instance, IdKey):
            return instance

        return cls(*identity_key(instance=instance))

    def get(self, _session: _sao.Session, **kw) -> T | None:
        """
        Shortcut for ``session.get(k.mapped, k.key, identity_token=k.identity_token)``.
        """
        return _session.get(self.mapped, self.key, identity_token=self.identity_token, **kw)

    def get_one(self, _session: _sao.Session, **kw) -> T:
        """
        Like :meth:`get`, but raises :exc:`sqlalchemy.exc.NoResultFound` if no row is found.
        """
        if (inst := self.get(_session, **kw)) is None:
            raise NoResultFound("No row was found when one was required")
        return inst


@dataclasses.dataclass
class RemoteWrapper:
    _object_: object

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __getitem__(self, name):
        value = getattr(self._object_, name)
        if isinstance(value, ColumnCollection):
            return RemoteWrapper(value)
        else:
            return _sao.remote(value)


@dataclasses.dataclass(eq=False)
class Relationships:
    """
    Generates pairs of relationships. It's like the legacy "backref" parameter but it allows you to configure each side
    of the relationship separately.

    For example::

        _rel_children_parent = _orm.Relationships(
            lambda: dict(a=Parent, b=Child),
            dict(ab="children", ba="parent"),
            lambda fk, a, b: a.id == fk(b.parent_id),
        )


        class Parent(Base):
            __tablename__ = "parent"

            id = sa.Column(sa.Integer, primary_key=True)

            children = _rel_children_parent.a_to_b(viewonly=True)


        class Child(Base):
            __tablename__ = "child"

            id = sa.Column(sa.Integer, primary_key=True)
            parent_id = sa.Column(sa.ForeignKey("parent.id"))

            parent = _rel_children_parent.b_to_a(viewonly=True)
    """

    tables: ty.Callable
    names: dict[str, str]
    primary: ty.Callable
    secondary: ty.Callable | None = dataclasses.field(default=None)
    kwargs: dict = dataclasses.field(default_factory=dict)

    def _make_relationship_kwargs(self, keys_only: bool):
        fk = _sao.foreign
        R = RemoteWrapper

        if keys_only:
            primary = secondary = lambda *args, **kwargs: None
        else:
            primary = self.primary
            secondary = self.secondary
            tables = self.tables()

        a = None if keys_only else tables["a"]
        b = None if keys_only else tables["b"]
        if self.secondary is None:
            return dict(
                ab=dict(argument=b, primaryjoin=primary(fk=fk, a=a, b=R(b))),
                ba=dict(argument=a, primaryjoin=primary(fk=fk, a=R(a), b=b)),
            )
        else:
            m = None if keys_only else tables["m"]
            am = primary(fk=fk, a=a, b=b, m=R(m))
            bm = secondary(fk=fk, a=a, b=b, m=R(m))
            return dict(
                ab=dict(argument=b, secondary=m, primaryjoin=am, secondaryjoin=bm),
                ba=dict(argument=a, secondary=m, primaryjoin=bm, secondaryjoin=am),
                # commented out because SQLAlchemy doesn't like it when the association table is a mapped class
                # am=dict(argument=m, primaryjoin=am),
                # ma=dict(argument=a, primaryjoin=primary(fk=fk, a=R(a), b=b, m=m)),
                # bm=dict(argument=m, primaryjoin=bm),
                # mb=dict(argument=b, primaryjoin=primary(fk=fk, a=a, b=R(b), m=m)),
            )

    @functools.cached_property
    def _cached_relationship_kwargs(self):
        return self._make_relationship_kwargs(False)

    @functools.cached_property
    def _cached_relationship_kwargs_keys(self):
        return self._make_relationship_kwargs(True)

    def _make_relationship_lazy_kwargs(self, case: str):
        keys = self._cached_relationship_kwargs_keys

        def _make_lambda(key: str):
            return lambda: self._cached_relationship_kwargs[case][key]

        kw = {k: _make_lambda(k) for k in keys[case]}
        if reverse_name := self.names.get(case[::-1]):
            kw["back_populates"] = reverse_name
        return kw

    def _make_relationship(self, case: str, kwargs):
        return _sao.relationship(**self._make_relationship_lazy_kwargs(case), **self.kwargs, **kwargs)

    def a_to_b(self, **kwargs):
        return self._make_relationship("ab", kwargs)

    def b_to_a(self, **kwargs):
        return self._make_relationship("ba", kwargs)

    # def a_to_m(self, **kwargs):
    #     return self._make_relationship("am", kwargs)

    # def m_to_a(self, **kwargs):
    #     return self._make_relationship("ma", kwargs)

    # def b_to_m(self, **kwargs):
    #     return self._make_relationship("bm", kwargs)

    # def m_to_b(self, **kwargs):
    #     return self._make_relationship("mb", kwargs)
