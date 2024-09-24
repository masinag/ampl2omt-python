import pytest

from ampl2omt.parsing.builder import ProblemBuilder
from ampl2omt.parsing.nlparser import NLParser
from ampl2omt.term.term import Term
from tests.unit.conftest import mgr


@pytest.fixture(scope='module')
def parser(mgr):
    return NLParser(mgr)


@pytest.fixture(scope='function')
def builder(mgr):
    return ProblemBuilder(mgr)


@pytest.fixture
def x(mgr) -> dict[int, Term]:
    return {i: mgr.VarReal(f"x{i}") for i in range(9)}


@pytest.fixture
def defs(mgr, x):
    n_vars = len(x)
    # t[i] = x[i]^2 + 1 + sum{j in 8..9} (i+j)*x[j];
    return {
        n_vars + i: mgr.Sum([mgr.Pow(x[i], mgr.Real(2)), mgr.Real(1),
                             mgr.Sum([mgr.Mult(mgr.Real(i + j + 2), x[j])
                                      for j in range(7, 9)])])
        for i in range(3)
    }


@pytest.fixture
def constraints(mgr, x, defs):
    return {
        0: mgr.Le(mgr.Plus(defs[10], mgr.Sin(defs[11])), mgr.Real(4)),
        1: mgr.Ge(mgr.Plus(x[4], mgr.Cos(x[5])), mgr.Real(3)),
        2: mgr.Eq(mgr.Sum([mgr.Mult(mgr.Real(i), x[i]) for i in range(2, 7)]), mgr.Real(1)),
        3: mgr.Ge(mgr.Plus(mgr.Pow(x[0], mgr.Real(2)), mgr.Pow(x[1], mgr.Real(2))),
                  mgr.Real(1)),
    }
