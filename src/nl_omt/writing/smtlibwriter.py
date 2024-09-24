from nl_omt.problem.problem import NLPProblem
from nl_omt.term.term import Term, topo_sort


class SmtlibWriter:

    def declare_vars(self, problem: NLPProblem) -> str:
        return "\n".join(f"(declare-fun {v.payload} () Real)" for v in problem.variables)

    def term_to_string(self, term: Term) -> str:
        bindings = []
        definitions: dict[Term, str] = {}
        n_defs = 0
        for node in topo_sort(term):
            if len(node.children) == 0:
                definition = str(node.payload)
            else:
                definition = f".def_{n_defs}"
                n_defs += 1
                bindings.append(f"(let (({definition} {self.term_to_string_short(node, definitions)}))")
            definitions[node] = definition

        bindings.append(f"{definitions[term]}")
        term_str = ' '.join(bindings) + ')' * (len(bindings) - 1)
        return term_str

    def term_to_string_short(self, term: Term, definitions: dict[Term, str]) -> str:
        assert len(term.children) > 0
        return f"({term.term_type.name} {' '.join(definitions[c] for c in term.children)})"
