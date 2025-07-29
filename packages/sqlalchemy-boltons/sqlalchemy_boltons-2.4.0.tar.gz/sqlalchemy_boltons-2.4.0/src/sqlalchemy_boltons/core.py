from __future__ import annotations

import sqlalchemy as sa


__all__ = ["count1", "bytes_startswith", "bytes_prefix_upper_bound"]

_SQLExpression = object


def bytes_prefix_upper_bound(prefix: bytes) -> bytes | None:
    stripped = prefix.rstrip(b"\xff")
    if not stripped:
        return None
    return b"".join((memoryview(stripped)[:-1], bytes((stripped[-1] + 1,))))


def bytes_startswith(operand: _SQLExpression, prefix: bytes) -> _SQLExpression:
    """
    Produces SQL equivalent to ``operand.startswith(prefix)``, but which works correctly for BLOB-like columns.

    As an example, the resulting SQL for ``bytes_startswith(x, b"abc")`` is something like
    ``(x >= b"abc") & (x < b"abd")``.
    """
    expr = operand >= prefix
    if upper := bytes_prefix_upper_bound(prefix):
        expr = expr & (operand < upper)
    return expr


def count1(select_from=None):
    """
    Produces ``COUNT(1)``. You can use this as a replacement for ``sqlalchemy.func.count()`` which produces ``COUNT(*)``
    instead.
    """
    expr = sa.func.count(sa.text("1"))
    return expr if select_from is None else expr.select_from(select_from)
