import io

import pytest

from ampl2omt.parsing.stream import LineStream
from ampl2omt.problem.objective import Objective


def test_parse_function_segment(mgr, parser, builder):
    segment = LineStream(io.StringIO("F0 1 -1 myfunc"))
    with pytest.raises(NotImplementedError):
        parser.parse_segment(segment, builder)


def test_parse_suffix_segment(mgr, parser, builder):
    segment = LineStream(io.StringIO("""S0 8 zork
    0 2
    1 6
    2 7
    3 8
    4 9
    5 3
    6 5
    8 4"""))
    with pytest.raises(NotImplementedError):
        parser.parse_segment(segment, builder)


def test_parse_definition_segment(mocker, mgr, builder, parser, x):
    segment = LineStream(io.StringIO("""V9 0 0 # defs[9]
    o5 # ^
    v0 # x[0]
    n2"""))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    parser.parse_segment(segment, builder)
    assert builder.get_definition(9) == mgr.Pow(x[0], mgr.Real(2))
    segment = LineStream(io.StringIO("""V10 2 0 #defs[10]
    3 10 # x[3] * 10 + 
    4 11 # x[4] * 11 +
    o0 # +
    v9 # defs[9]
    n1"""))
    parser.parse_segment(segment, builder)
    assert builder.get_definition(10) == mgr.Sum([mgr.Mult(x[3], mgr.Real(10)),
                                                  mgr.Mult(x[4], mgr.Real(11)),
                                                  mgr.Plus(builder.get_definition(9), mgr.Real(1))])
    assert segment.peek() == ""


def test_parse_cons_body_segment(mocker, mgr, builder, parser, x):
    segment = LineStream(io.StringIO("""C1
    o0 # +
    v5 # x[5]
    o46 # cos
    v6 # x[6]"""))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    parser.parse_segment(segment, builder)
    assert builder.cons_body[1] == mgr.Plus(x[5], mgr.Cos(x[6]))
    assert segment.peek() == ""


def test_parse_objective_segment(mocker, mgr, builder, parser, x, defs):
    segment = LineStream(io.StringIO("""O0 1 #zip
    o35 # if
    o28 # >=
    v10 #t[2]
    n0
    o16 #-
    o5 #^
    v10 #t[2]
    n3
    o16 #-
    o5 #^
    v10 #t[2]
    n2"""))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    mocker.patch.object(builder, "get_definition", side_effect=defs.get)

    parser.parse_segment(segment, builder)
    expected = Objective(Objective.MAXIMIZE, mgr.If(
        mgr.Ge(builder.get_definition(10), mgr.Real(0)),
        mgr.Neg(mgr.Pow(builder.get_definition(10), mgr.Real(3))),
        mgr.Neg(mgr.Pow(builder.get_definition(10), mgr.Real(2)))
    ))
    assert builder.get_obj(0) == expected
    assert segment.peek() == ""


def test_parse_ranges_segment(mocker, mgr, builder, parser, constraints):
    segment = LineStream(io.StringIO("""r #4 ranges (rhs's)
    1 3
    2 3
    0 4.3 15.5
    4 1"""))
    mocker.patch.object(builder, "get_cons_body", side_effect=constraints.get)
    builder.n_cons = len(constraints)
    parser.parse_segment(segment, builder)
    assert builder.cons_ranges == {
        0: (None, 3.),
        1: (3., None),
        2: (4.3, 15.5),
        3: (1., 1.)
    }
    assert segment.peek() == ""


def test_parse_var_bounds_segment(mocker, mgr, builder, parser, x):
    segment = LineStream(io.StringIO("""b #4 var bounds
    1 3
    2 3
    0 4.3 15.5
    4 1"""))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    builder.n_vars = 4
    parser.parse_segment(segment, builder)
    assert builder.var_ranges == {
        0: (None, 3.),
        1: (3., None),
        2: (4.3, 15.5),
        3: (1., 1.)
    }
    assert segment.peek() == ""


def test_parse_jacobian_column_counts_segment(builder, parser):
    segment = LineStream(io.StringIO("""k8 #intermediate Jacobian column lengths
    2
    5
    6
    8
    10
    13
    16
    16"""))
    builder.n_vars = 9
    parser.parse_segment(segment, builder)
    assert segment.peek() == ""


def test_parse_jacobian_sparsity_segment(builder, parser):
    segment = LineStream(io.StringIO("""J0 4
    0 0
    3 10
    4 11
    5 0"""))
    parser.parse_segment(segment, builder)
    assert segment.peek() == ""


def test_parse_gradient_sparsity_segment(builder, parser):
    segment = LineStream(io.StringIO("""G0 4
    0 0
    3 10
    4 11
    5 0"""))
    parser.parse_segment(segment, builder)
    assert segment.peek() == ""
