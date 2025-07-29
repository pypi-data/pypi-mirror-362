import dataclasses

from sqlalchemy_boltons.core import bytes_startswith


class Expr:
    """Mock expression class used for testing."""

    @classmethod
    def make_variable(cls, name):
        return cls(("var", name))

    def __eq__(self, other):
        return BinaryOp(self, "==", other)

    def __ne__(self, other):
        return BinaryOp(self, "!=", other)

    def __lt__(self, other):
        return BinaryOp(self, "<", other)

    def __le__(self, other):
        return BinaryOp(self, "<=", other)

    def __gt__(self, other):
        return BinaryOp(other, "<", self)

    def __ge__(self, other):
        return BinaryOp(other, "<=", self)

    def __and__(self, other):
        return BinaryOp(self, "&", other)


@dataclasses.dataclass
class Var(Expr):
    name: str

    def __repr__(self):
        return self.name


@dataclasses.dataclass
class BinaryOp(Expr):
    left: object
    op: str
    right: object

    def __repr__(self):
        return f"({self.left!r} {self.op} {self.right!r})"


def test_bytes_startswith():
    x = Var("x")
    assert bytes_startswith(x, b"aaa") == (x >= b"aaa") & (x < b"aab"), "get upper bound by incrementing last byte"
    assert bytes_startswith(x, b"aaa") != (x >= b"aaa") & (x < b"aaz"), "check that eq operator even works correctly"
    assert bytes_startswith(x, b"abc") == (x >= b"abc") & (x < b"abd")
    assert bytes_startswith(x, b"aaa\xff\xff") == (x >= b"aaa\xff\xff") & (
        x < b"aab"
    ), "if a string ends with 0xFF, then increment the first non-0xFF byte from the right"
    assert bytes_startswith(x, b"\xff\xff") == (x >= b"\xff\xff"), "all-0xFF bytestring has no upper bound"
