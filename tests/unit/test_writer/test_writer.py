from nl_omt.problem.problem import NLPProblem


def test_write_vars(writer, x):
    problem = NLPProblem(
        variables=x[:4],
        constraints=[],
        objectives=[],
    )
    assert writer.declare_vars(problem) == """(declare-fun x0 () Real)
(declare-fun x1 () Real)
(declare-fun x2 () Real)
(declare-fun x3 () Real)"""


def test_var_to_string(writer, x):
    assert writer.term_to_string(x[0]) == "x0"


def test_const_to_string(mgr, writer):
    assert writer.term_to_string(mgr.Real(1.0)) == "1.0"


def test_flat_op_to_string(mgr, writer, x):
    term = mgr.Plus(x[0], x[1])
    assert writer.term_to_string(term) == "(let ((.def_0 (+ x0 x1))) .def_0)"


def test_nested_op_to_string(mgr, writer, x):
    term = mgr.Plus(mgr.Plus(x[0], x[1]), x[2])
    assert writer.term_to_string(term) == "(let ((.def_0 (+ x0 x1))) (let ((.def_1 (+ .def_0 x2))) .def_1))"


def test_deeply_nested_to_string(mgr, writer, x):
    term = mgr.Le(
        mgr.Plus(
            mgr.Mult(mgr.Real(2), x[0]),
            mgr.Plus(mgr.Mult(x[0], x[1]), mgr.Real(1))
        ),
        mgr.Plus(
            mgr.Neg(x[0]),
            mgr.Mult(x[0], x[1])
        )
    )
    assert (writer.term_to_string(term) ==
            "(let ((.def_0 (* 2 x0))) (let ((.def_1 (* x0 x1))) (let ((.def_2 (+ .def_1 1))) (let ((.def_3 (+ .def_0 .def_2))) (let ((.def_4 (- x0))) (let ((.def_5 (* x0 x1))) (let ((.def_6 (+ .def_4 .def_5))) (let ((.def_7 (<= .def_3 .def_6))) .def_7))))))))")
