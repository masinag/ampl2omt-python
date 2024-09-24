import io

import pytest

from nl_omt.parsing.stream import LineStream
from nl_omt.problem.objective import Objective
from nl_omt.term.term import Term


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


def test_constant(manager, parser, builder):
    segment = LineStream(io.StringIO("n1e-1"))
    term = parser.parse_expression(segment, builder)
    assert term == manager.Real(0.1)


def test_variable(mocker, manager, builder, parser, x):
    segment = LineStream(io.StringIO("v1"))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    term = parser.parse_expression(segment, builder)
    assert term == x[1]


def test_definition(mocker, manager, builder, parser, x, defs):
    segment = LineStream(io.StringIO("v10"))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_definition", side_effect=defs.get)
    term = parser.parse_expression(segment, builder)
    assert term == defs[10]


def test_function(manager, parser, builder):
    segment = LineStream(io.StringIO("f1"))
    with pytest.raises(NotImplementedError):
        parser.parse_expression(segment, builder)


def test_expression(mocker, manager, builder, parser, x, defs):
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
    expected = manager.Sinh(
        manager.Sum([x[7], manager.Mult(manager.Real(2), defs[10]), manager.Mult(manager.Real(6), x[1])]))
    assert term == expected


def test_parse_definition_segment(mocker, manager, builder, parser, x):
    segment = LineStream(io.StringIO("""V9 0 0 # defs[9]
    o5 # ^
    v0 # x[0]
    n2"""))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    parser.parse_segment(segment, builder)
    assert builder.get_definition(9) == manager.Pow(x[0], manager.Real(2))
    segment = LineStream(io.StringIO("""V10 2 0 #defs[10]
    3 10 # x[3] * 10 + 
    4 11 # x[4] * 11 +
    o0 # +
    v9 # defs[9]
    n1"""))
    parser.parse_segment(segment, builder)
    assert builder.get_definition(10) == manager.Sum([manager.Mult(x[3], manager.Real(10)),
                                                      manager.Mult(x[4], manager.Real(11)),
                                                      manager.Plus(builder.get_definition(9), manager.Real(1))])


def test_parse_cons_body_segment(mocker, manager, builder, parser, x):
    segment = LineStream(io.StringIO("""C1
    o0 # +
    v5 # x[5]
    o46 # cos
    v6 # x[6]"""))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    parser.parse_segment(segment, builder)
    assert builder.cons_body[1] == manager.Plus(x[5], manager.Cos(x[6]))


def test_parse_objective_segment(mocker, manager, builder, parser, x, defs):
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
    expected = Objective(Objective.MAXIMIZE, manager.If(
        manager.Ge(builder.get_definition(10), manager.Real(0)),
        manager.Neg(manager.Pow(builder.get_definition(10), manager.Real(3))),
        manager.Neg(manager.Pow(builder.get_definition(10), manager.Real(2)))
    ))
    assert builder.get_obj(0) == expected


def test_parse_ranges_segment(mocker, manager, builder, parser, x, constraints):
    segment = LineStream(io.StringIO("""r #4 ranges (rhs's)
    1 3
    2 3
    0 4.3 15.5
    4 1"""))
    mocker.patch.object(builder, "is_problem_var", side_effect=lambda i: i in x)
    mocker.patch.object(builder, "get_problem_var", side_effect=x.get)
    mocker.patch.object(builder, "get_cons_body", side_effect=constraints.get)
    builder.n_cons = len(constraints)
    parser.parse_segment(segment, builder)
    assert builder.ranges == [manager.Le(constraints[0], manager.Real(3)),
                              manager.Ge(constraints[1], manager.Real(3)),
                              manager.And(manager.Ge(constraints[2], manager.Real(4.3)),
                                          manager.Le(constraints[2], manager.Real(15.5))),
                              manager.Eq(constraints[3], manager.Real(1))]
