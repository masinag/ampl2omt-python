import pytest

from nl_omt.expression.factory import NodeFactory
from nl_omt.expression.node import Kind


@pytest.fixture
def factory():
    return NodeFactory()


@pytest.fixture
def one(factory):
    return factory.create_constant(Kind.REAL, 1)


@pytest.fixture
def two(factory):
    return factory.create_constant(Kind.REAL, 2)


@pytest.mark.parametrize("method, kind", [
    ("Real", Kind.REAL),
    ("Int", Kind.INT),
    ("Bool", Kind.BOOL),
])
def test_constants(factory, method, kind):
    assert getattr(factory, method)(1).kind == kind


@pytest.mark.parametrize("method, kind", [
    ("VarReal", Kind.VAR_REAL),
    ("VarInt", Kind.VAR_INT),
    ("VarBool", Kind.VAR_BOOL),
])
def test_variables(factory, method, kind):
    assert getattr(factory, method)("x").kind == kind


@pytest.mark.parametrize("method, kind", [
    ("Floor", Kind.FLOOR),
    ("Ceil", Kind.CEIL),
    ("Abs", Kind.ABS),
    ("Neg", Kind.NEG),
    ("Not", Kind.NOT),
    ("Tanh", Kind.TANH),
    ("Tan", Kind.TAN),
    ("Sqrt", Kind.SQRT)
])
def test_unary_operators(factory, one, method, kind):
    assert getattr(factory, method)(one).kind == kind


@pytest.mark.parametrize("method, kind", [
    ("Plus", Kind.PLUS),
    ("Minus", Kind.MINUS),
    ("Mult", Kind.MULT),
    ("Div", Kind.DIV),
    ("Rem", Kind.REM),
    ("Pow", Kind.POW),
    ("Less", Kind.LESS),
    ("Or", Kind.OR),
    ("And", Kind.AND),
    ("Lt", Kind.LT),
    ("Le", Kind.LE),
    ("Eq", Kind.EQ),
    ("Ge", Kind.GE),
    ("Gt", Kind.GT),
    ("Ne", Kind.NE),
    ("Atan2", Kind.ATAN2),
    ("IntDiv", Kind.INTDIV),
    ("Precision", Kind.PRECISION),
    ("Round", Kind.ROUND),
    ("Trunc", Kind.TRUNC),
    ("Iff", Kind.IFF)
])
def test_binary_operators(factory, one, two, method, kind):
    assert getattr(factory, method)(one, two).kind == kind


@pytest.mark.parametrize("method, kind", [
    ("Min", Kind.MIN),
    ("Max", Kind.MAX),
    ("Sum", Kind.SUM),
    ("Count", Kind.COUNT),
    ("NumberOf", Kind.NUMBEROF)
])
def test_nary_operators(factory, one, two, method, kind):
    assert getattr(factory, method)([one, two]).kind == kind


def test_cached_constants(factory):
    node1 = factory.Real(1)
    node2 = factory.Real(1)
    assert node1 is node2


def test_cached_variables(factory):
    node1 = factory.VarReal("x")
    node2 = factory.VarReal("x")
    assert node1 is node2


def test_cached_unary_operators(factory, one):
    node1 = factory.Floor(one)
    node2 = factory.Floor(one)
    assert node1 is node2


def test_cached_binary_operators(factory, one, two):
    node1 = factory.Plus(one, two)
    node2 = factory.Plus(one, two)
    assert node1 is node2


def test_cached_nary_operators(factory, one, two):
    node1 = factory.Min([one, two])
    node2 = factory.Min([one, two])
    assert node1 is node2
