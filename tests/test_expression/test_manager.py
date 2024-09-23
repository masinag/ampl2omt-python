import pytest

from nl_omt.term import types
from nl_omt.term.manager import TermManager


@pytest.fixture
def manager():
    return TermManager()


@pytest.fixture
def one(manager):
    return manager.Real(1)


@pytest.fixture
def two(manager):
    return manager.Real(2)


@pytest.mark.parametrize("method, term_type", [
    ("Real", types.REAL),
    ("Int", types.INT),
    ("Bool", types.BOOL),
])
def test_constants(manager, method, term_type):
    assert getattr(manager, method)(1).term_type == manager.term_type(term_type)


@pytest.mark.parametrize("method, term_type", [
    ("VarReal", types.VAR_REAL),
    ("VarInt", types.VAR_INT),
    ("VarBool", types.VAR_BOOL),
])
def test_variables(manager, method, term_type):
    assert getattr(manager, method)("x").term_type == manager.term_type(term_type)


@pytest.mark.parametrize("method, term_type", [
    ("Floor", types.FLOOR),
    ("Ceil", types.CEIL),
    ("Abs", types.ABS),
    ("Neg", types.NEG),
    ("Not", types.NOT),
    ("Tanh", types.TANH),
    ("Tan", types.TAN),
    ("Sqrt", types.SQRT)
])
def test_unary_operators(manager, one, method, term_type):
    assert getattr(manager, method)(one).term_type == manager.term_type(term_type)


@pytest.mark.parametrize("method, term_type", [
    ("Plus", types.PLUS),
    ("Minus", types.MINUS),
    ("Mult", types.MULT),
    ("Div", types.DIV),
    ("Rem", types.REM),
    ("Pow", types.POW),
    # ("Less", types.LESS),
    ("Or", types.OR),
    ("And", types.AND),
    ("Lt", types.LT),
    ("Le", types.LE),
    ("Eq", types.EQ),
    ("Ge", types.GE),
    ("Gt", types.GT),
    ("Ne", types.NE),
    ("Atan2", types.ATAN2),
    ("IntDiv", types.INTDIV),
    ("Precision", types.PRECISION),
    ("Round", types.ROUND),
    ("Trunc", types.TRUNC),
    ("Iff", types.IFF)
])
def test_binary_operators(manager, one, two, method, term_type):
    assert getattr(manager, method)(one, two).term_type == manager.term_type(term_type)


@pytest.mark.parametrize("method, term_type", [
    ("Min", types.MIN),
    ("Max", types.MAX),
    ("Sum", types.SUM),
    ("Count", types.COUNT),
    ("NumberOf", types.NUMBEROF)
])
def test_nary_operators(manager, one, two, method, term_type):
    assert getattr(manager, method)([one, two]).term_type == manager.term_type(term_type)


def test_cached_constants(manager):
    node1 = manager.Real(1)
    node2 = manager.Real(1)
    assert node1 is node2


def test_cached_variables(manager):
    node1 = manager.VarReal("x")
    node2 = manager.VarReal("x")
    assert node1 is node2


def test_cached_unary_operators(manager, one):
    node1 = manager.Floor(one)
    node2 = manager.Floor(one)
    assert node1 is node2


def test_cached_binary_operators(manager, one, two):
    node1 = manager.Plus(one, two)
    node2 = manager.Plus(one, two)
    assert node1 is node2


def test_cached_nary_operators(manager, one, two):
    node1 = manager.Min([one, two])
    node2 = manager.Min([one, two])
    assert node1 is node2
