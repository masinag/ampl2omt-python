import pytest

from ampl2omt.term import types


@pytest.fixture
def one(mgr):
    return mgr.Real(1)


@pytest.fixture
def two(mgr):
    return mgr.Real(2)


@pytest.mark.parametrize("method, term_type", [
    ("Real", types.REAL),
    ("Int", types.INT),
    ("Bool", types.BOOL),
])
def test_constants(mgr, method, term_type):
    assert getattr(mgr, method)(1).term_type == mgr.term_type(term_type)


@pytest.mark.parametrize("method, term_type", [
    ("VarReal", types.VAR_REAL),
    ("VarInt", types.VAR_INT),
    ("VarBool", types.VAR_BOOL),
])
def test_variables(mgr, method, term_type):
    assert getattr(mgr, method)("x").term_type == mgr.term_type(term_type)


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
def test_unary_operators(mgr, one, method, term_type):
    assert getattr(mgr, method)(one).term_type == mgr.term_type(term_type)


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
def test_binary_operators(mgr, one, two, method, term_type):
    assert getattr(mgr, method)(one, two).term_type == mgr.term_type(term_type)


@pytest.mark.parametrize("method, term_type", [
    ("Min", types.MIN),
    ("Max", types.MAX),
    ("Sum", types.SUM),
    ("Count", types.COUNT),
    ("NumberOf", types.NUMBEROF)
])
def test_nary_operators(mgr, one, two, method, term_type):
    assert getattr(mgr, method)([one, two]).term_type == mgr.term_type(term_type)


def test_cached_constants(mgr):
    node1 = mgr.Real(1)
    node2 = mgr.Real(1)
    assert node1 is node2


def test_cached_variables(mgr):
    node1 = mgr.VarReal("x")
    node2 = mgr.VarReal("x")
    assert node1 is node2


def test_cached_unary_operators(mgr, one):
    node1 = mgr.Floor(one)
    node2 = mgr.Floor(one)
    assert node1 is node2


def test_cached_binary_operators(mgr, one, two):
    node1 = mgr.Plus(one, two)
    node2 = mgr.Plus(one, two)
    assert node1 is node2


def test_cached_nary_operators(mgr, one, two):
    node1 = mgr.Min([one, two])
    node2 = mgr.Min([one, two])
    assert node1 is node2
