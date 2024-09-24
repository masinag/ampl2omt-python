from ampl2omt.problem.objective import Objective
from ampl2omt.problem.problem import NLPProblem
from ampl2omt.term.term import Term, topo_sort


class SmtlibWriter:
    def to_smtlib(self, problem: NLPProblem, daggify=False) -> str:
        return ("(set-logic QF_NRAT)\n"
                "(set-option :produce-models true)\n\n"
                f"{self.declare_vars(problem)}\n\n"
                f"{self.declare_constraints(problem, False)}\n\n"
                f"{self.declare_objectives(problem, False)}\n\n"
                f"(check-sat)\n"
                f"(get-objectives)")

    def declare_vars(self, problem: NLPProblem) -> str:
        return "\n".join(f"(declare-fun {v.payload} () Real)" for v in problem.variables)

    def declare_constraints(self, problem: NLPProblem, daggify) -> str:
        return "\n".join(
            f"(assert {self.term_to_string(c, daggify)})"
            for c in problem.constraints
        )

    def declare_objectives(self, problem: NLPProblem, daggify) -> str:
        return "\n".join(
            f"(minimize {self.term_to_string(o.term, daggify)})" if o.kind == Objective.MINIMIZE else
            f"(maximize {self.term_to_string(o.term, daggify)})"
            for o in problem.objectives
        )

    def term_to_string(self, term: Term, daggify) -> str:
        bindings = []
        definitions: dict[Term, str] = {}
        n_defs = 0
        for node in topo_sort(term):
            if len(node.children) == 0:
                definition = str(node.payload)
            else:
                if daggify:
                    definition = f".def_{n_defs}"
                    n_defs += 1
                    bindings.append(f"(let (({definition} {self.term_to_string_def(node, definitions)}))")
                else:
                    definition = self.term_to_string_def(node, definitions)
            definitions[node] = definition

        bindings.append(f"{definitions[term]}")
        term_str = ' '.join(bindings) + ')' * (len(bindings) - 1)
        return term_str

    def term_to_string_def(self, term: Term, definitions: dict[Term, str]) -> str:
        assert len(term.children) > 0
        return f"({term.term_type.name} {' '.join(definitions[c] for c in term.children)})"
