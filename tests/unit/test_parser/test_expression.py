import io

import pytest

from ampl2omt.parsing.stream import LineStream


def test_constant(mgr, parser, builder):
    segment = LineStream(io.StringIO("n1e-1"))
    term = parser.parse_expression(segment, builder)
    assert term == mgr.Real(0.1)
    assert segment.peek() == ""


def test_variable(mocker, mgr, builder, parser, x):
    segment = LineStream(io.StringIO("v1"))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    term = parser.parse_expression(segment, builder)
    assert term == x[1]
    assert segment.peek() == ""


def test_definition(mocker, mgr, builder, parser, x, defs):
    segment = LineStream(io.StringIO("v10"))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_definition", side_effect=defs.get)
    term = parser.parse_expression(segment, builder)
    assert term == defs[10]
    assert segment.peek() == ""


def test_function(mgr, parser, builder):
    segment = LineStream(io.StringIO("f1"))
    with pytest.raises(NotImplementedError):
        parser.parse_expression(segment, builder)


def test_expression(mocker, mgr, builder, parser, x, defs):
    segment = LineStream(io.StringIO("""o40 # sinh
    o54 # sumlist
    3
    v7 # x[7]
    o2 # *
    n2
    v10 # defs[10]
    o2 # *
    n6
    v1 # x[1]"""))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    mocker.patch.object(builder, "get_definition", side_effect=defs.get)
    term = parser.parse_expression(segment, builder)
    expected = mgr.Sinh(
        mgr.Sum([x[7], mgr.Mult(mgr.Real(2), defs[10]), mgr.Mult(mgr.Real(6), x[1])]))
    assert term == expected
    assert segment.peek() == ""
