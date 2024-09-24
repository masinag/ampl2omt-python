from nl_omt.problem.objective import Objective
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


def test_var_to_string_dag(writer, x):
    assert writer.term_to_string(x[0], daggify=True) == "x0"


def test_var_to_string_no_dag(writer, x):
    assert writer.term_to_string(x[0], daggify=False) == "x0"


def test_const_to_string_dag(mgr, writer):
    assert writer.term_to_string(mgr.Real(1.0), daggify=True) == "1.0"


def test_const_to_string_no_dag(mgr, writer):
    assert writer.term_to_string(mgr.Real(1.0), daggify=False) == "1.0"


def test_flat_op_to_string_dag(mgr, writer, x):
    term = mgr.Plus(x[0], x[1])
    assert writer.term_to_string(term, daggify=True) == "(let ((.def_0 (+ x0 x1))) .def_0)"


def test_flat_op_to_string_no_dag(mgr, writer, x):
    term = mgr.Plus(x[0], x[1])
    assert writer.term_to_string(term, daggify=False) == "(+ x0 x1)"


def test_nested_op_to_string_dag(mgr, writer, x):
    term = mgr.Plus(mgr.Plus(x[0], x[1]), x[2])
    assert writer.term_to_string(term,
                                 daggify=True) == "(let ((.def_0 (+ x0 x1))) (let ((.def_1 (+ .def_0 x2))) .def_1))"


def test_nested_op_to_string_no_dag(mgr, writer, x):
    term = mgr.Plus(mgr.Plus(x[0], x[1]), x[2])
    assert writer.term_to_string(term, daggify=False) == "(+ (+ x0 x1) x2)"


def test_deeply_nested_to_string_dag(mgr, writer, x):
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
    assert (writer.term_to_string(term, daggify=True) ==
            "(let ((.def_0 (* 2.0 x0))) (let ((.def_1 (* x0 x1))) (let ((.def_2 (+ .def_1 1.0))) (let ((.def_3 (+ .def_0 .def_2))) (let ((.def_4 (- x0))) (let ((.def_5 (* x0 x1))) (let ((.def_6 (+ .def_4 .def_5))) (let ((.def_7 (<= .def_3 .def_6))) .def_7))))))))")


def test_deeply_nested_to_string_no_dag(mgr, writer, x):
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
    assert (writer.term_to_string(term, daggify=False) ==
            "(<= (+ (* 2.0 x0) (+ (* x0 x1) 1.0)) (+ (- x0) (* x0 x1)))")


def test_to_smtlib(mgr, writer, x):
    problem = NLPProblem(
        variables=x[:3],
        constraints=[
            mgr.Le(x[0], x[1]),
            mgr.Ge(x[2], mgr.Real(0)),
            mgr.Eq(x[3], mgr.Sin(mgr.Mult(mgr.Real(2), x[3])))
        ],
        objectives=[
            Objective(Objective.MINIMIZE, x[0]),
            Objective(Objective.MAXIMIZE, mgr.Mult(mgr.Plus(x[1], x[2]), x[3]))
        ],
    )
    assert (writer.to_smtlib(problem) ==
            "(set-logic QF_NRAT)\n"
            "(set-option :produce-models true)\n\n"
            "(declare-fun x0 () Real)\n"
            "(declare-fun x1 () Real)\n"
            "(declare-fun x2 () Real)\n\n"
            "(assert (<= x0 x1))\n"
            "(assert (>= x2 0.0))\n"
            "(assert (= x3 (sin (* 2.0 x3))))\n\n"
            "(minimize x0)\n"
            "(maximize (* (+ x1 x2) x3))\n\n"
            "(check-sat)\n"
            "(get-objectives)")
