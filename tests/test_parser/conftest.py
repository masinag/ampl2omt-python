import pytest

from nl_omt.parsing.builder import ProblemBuilder
from nl_omt.parsing.nlparser import NLParser
from nl_omt.term.manager import TermManager
from nl_omt.term.term import Term


@pytest.fixture(scope='module')
def manager():
    return TermManager()


@pytest.fixture(scope='module')
def parser(manager):
    return NLParser(manager)


@pytest.fixture(scope='function')
def builder():
    return ProblemBuilder()


@pytest.fixture
def x(manager) -> dict[int, Term]:
    return {i: manager.VarReal(f"x{i}") for i in range(9)}


@pytest.fixture
def defs(manager, x):
    n_vars = len(x)
    # t[i] = x[i]^2 + 1 + sum{j in 8..9} (i+j)*x[j];
    return {
        n_vars + i: manager.Sum([manager.Pow(x[i], manager.Real(2)), manager.Real(1),
                                 manager.Sum([manager.Mult(manager.Real(i + j + 2), x[j])
                                              for j in range(7, 9)])])
        for i in range(3)
    }


@pytest.fixture
def constraints(manager, x, defs):
    return {
        0: manager.Le(manager.Plus(defs[10], manager.Sin(defs[11])), manager.Real(4)),
        1: manager.Ge(manager.Plus(x[4], manager.Cos(x[5])), manager.Real(3)),
        2: manager.Eq(manager.Sum([manager.Mult(manager.Real(i), x[i]) for i in range(2, 7)]), manager.Real(1)),
        3: manager.Ge(manager.Plus(manager.Pow(x[0], manager.Real(2)), manager.Pow(x[1], manager.Real(2))),
                      manager.Real(1)),
    }
