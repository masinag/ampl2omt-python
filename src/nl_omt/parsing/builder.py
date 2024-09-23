from nl_omt.problem.objective import Objective
from nl_omt.term.term import Term


class ProblemBuilder:
    def __init__(self):
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
        self.ranges: list[Term] = []
        self.eqs: list[Term] = []
        self.lns: list[Term] = []

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

    def get_range(self, i: int) -> Term:
        assert i < len(self.ranges), f"Range {i} not defined"
        return self.ranges[i]

    def with_range(self, term: Term):
        self.ranges.append(term)
        return self
