import io

import pytest

from nl_omt.expression.factory import NodeFactory
from nl_omt.nlparser import NLParser


@pytest.fixture(scope='module')
def factory():
    return NodeFactory()


@pytest.fixture(scope='function')
def parser(factory):
    return NLParser(factory)


def test_parse_header_success(parser):
    header = """g3 0 1 0	# problem a
 2 1 1 0 0	# vars, constraints, objectives, ranges, eqns
 1 1	# nonlinear constraints, objectives
 0 0	# network constraints: nonlinear, linear
 2 2 2	# nonlinear vars in constraints, objectives, both
 0 0 0 1	# linear network variables; functions; arith, flags
 0 0 0 0 0	# discrete variables: binary, integer, nonlinear (b,c,o)
 2 2	# nonzeros in Jacobian, gradients
 0 0	# max name lengths: constraints, variables
 0 0 0 0 0	# common exprs: b,c,o,c1,o1"""
    stream = io.StringIO(header)
    parser.parse_header(stream)

    assert parser.n_vars == 2
    assert parser.n_cons == 1
    assert parser.n_obj == 1
    assert parser.n_ranges == 0
    assert parser.n_eqs == 0

    assert len(parser.problem_vars) == 2


def test_parse_bad_header_first_line(parser):
    header = """b0 0 1 0	# problem a"""
    stream = io.StringIO(header)
    with pytest.raises(ValueError):
        parser.parse_header(stream)
