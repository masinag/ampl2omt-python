from ampl2omt.problem.objective import Objective
from ampl2omt.problem.problem import NLPProblem
from ampl2omt.term.manager import TermManager
from ampl2omt.term.term import Term, is_const


class ProblemBuilder:
    def __init__(self, mgr: TermManager):
        self.mgr = mgr

        self.n_vars: int = 0
        self.n_cons: int = 0
        self.n_obj: int = 0
        self.n_ranges: int = 0
        self.n_eqs: int = 0
        self.n_lns: int = 0

        self.problem_vars: dict[int, Term] = {}
        self.defined_vars: dict[int, Term] = {}

        self.cons_body: dict[int, Term] = {}
        self.obj: dict[int, Objective] = {}
        self.cons_ranges: dict[int, tuple[float | None, float | None]] = {}
        self.var_ranges: dict[int, tuple[float | None, float | None]] = {}
        self.lns: list[Term] = []

    def __repr__(self):
        return (f"ProblemBuilder("
                f"\tn_vars={self.n_vars},\n"
                f"\tn_cons={self.n_cons},\n"
                f"\tn_obj={self.n_obj},\n"
                f"\tn_ranges={self.n_ranges},\n"
                f"\tn_eqs={self.n_eqs},\n"
                f"\tn_lns={self.n_lns},\n"
                f"\tproblem_vars=\n\t\t{'\n\t\t'.join(map(str, self.problem_vars.values()))},\n"
                f"\tdefined_vars=\n\t\t{'\n\t\t'.join(map(str, self.defined_vars.values()))},\n"
                f"\tcons_body=\n\t\t{'\n\t\t'.join(map(str, self.cons_body.values()))},\n"
                f"\tobj=\n\t\t{'\n\t\t'.join(map(str, self.obj.values()))},\n"
                f"\tcons_ranges={self.cons_ranges.values()},\n"
                f"\tvar_ranges={self.var_ranges.values()},\n"
                f"\tlns={self.lns})")

    def with_n_vars(self, n_vars: int):
        self.n_vars = n_vars
        return self

    def with_n_cons(self, n_cons: int):
        self.n_cons = n_cons
        return self

    def with_n_obj(self, n_obj: int):
        self.n_obj = n_obj
        return self

    def with_n_ranges(self, n_ranges: int):
        self.n_ranges = n_ranges
        return self

    def with_n_eqs(self, n_eqs: int):
        self.n_eqs = n_eqs
        return self

    def with_n_lns(self, n_lns: int):
        self.n_lns = n_lns
        return self

    def get_problem_var(self, i: int) -> Term:
        assert i in self.problem_vars, f"Variable {i} not defined"
        return self.problem_vars[i]

    def is_problem_var(self, i: int) -> bool:
        return i in self.problem_vars

    def with_problem_var(self, i: int, term: Term):
        assert i not in self.problem_vars, f"Variable {i} is already defined"
        self.problem_vars[i] = term

    def get_definition(self, i: int) -> Term:
        assert i in self.defined_vars, f"Variable {i} not defined"
        return self.defined_vars[i]

    def with_definition(self, i: int, term: Term):
        assert i not in self.problem_vars, f"Variable {i} is a problem variable"
        assert i not in self.defined_vars, f"Variable {i} is already defined"
        self.defined_vars[i] = term
        return self

    def get_cons_body(self, i: int) -> Term:
        assert i in self.cons_body, f"Constraint {i} not defined"
        return self.cons_body[i]

    def with_cons_body(self, i: int, term: Term):
        self.cons_body[i] = term
        return self

    def get_obj(self, i: int) -> Objective:
        assert i < len(self.obj), f"Objective {i} not defined"
        return self.obj[i]

    def with_obj(self, i: int, obj: Objective):
        assert i not in self.obj, f"Objective {i} is already defined"
        self.obj[i] = obj
        return self

    def with_cons_range(self, i: int, lower: float | None, upper: float | None):
        self.cons_ranges[i] = (lower, upper)
        return self

    def with_var_range(self, i: int, lower: float | None, upper: float | None):
        self.var_ranges[i] = (lower, upper)
        return self

    def build_problem(self) -> NLPProblem:
        self._check_integrity()
        constraints = []
        for i, (lower, upper) in self.var_ranges.items():
            vi = self.get_problem_var(i)
            self._add_constraints(vi, lower, upper, constraints)

        for i, (lower, upper) in self.cons_ranges.items():
            ci = self.get_cons_body(i)
            self._add_constraints(ci, lower, upper, constraints)

        return NLPProblem(
            variables=list(self.problem_vars.values()),
            objectives=list(self.obj.values()),
            constraints=constraints,
        )

    def _add_constraints(self, vi, lower, upper, constraints):
        if is_const(vi):
            # The constraint has been simplified out (not sure)
            return
        if lower is None and upper is None:
            return
        if lower == upper:
            constraints.append(self.mgr.Eq(vi, self.mgr.Real(lower)))
        else:
            if lower is not None:
                constraints.append(self.mgr.Ge(vi, self.mgr.Real(lower)))
            if upper is not None:
                constraints.append(self.mgr.Le(vi, self.mgr.Real(upper)))

    def _check_integrity(self):
        assert len(self.problem_vars) == self.n_vars, f"Expected {self.n_vars} variables, got {len(self.problem_vars)}"
        assert len(self.cons_body) == self.n_cons, f"Expected {self.n_cons} constraints, got {len(self.cons_body)}"
        assert len(self.obj) == self.n_obj, f"Expected {self.n_obj} objectives, got {len(self.obj)}"
        n_eqs = sum(1 for l, u in self.cons_ranges.values() if l is not None and u is not None and l == u)
        n_rgs = sum(1 for l, u in self.cons_ranges.values() if l is not None and u is not None and l != u)
        assert n_eqs == self.n_eqs, f"Expected {self.n_eqs} equality constraints, got {n_eqs}"
        assert n_rgs == self.n_ranges, f"Expected {self.n_ranges} range constraints, got {n_rgs}"
        assert len(self.var_ranges) == self.n_vars, f"Expected {self.n_vars} var ranges, got {len(self.var_ranges)}"
