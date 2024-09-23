from dataclasses import dataclass

from nl_omt.term.term import Term


@dataclass
class Objective:
    """
    A class to represent an objective.

    :param name: The name of the objective.
    :param kind: The kind of the objective (MINIMIZE or MAXIMIZE).
    :param ExpressionGraph: The expression graph.
    """
    kind: int
    expression_graph: Term
    name: str | None = None

    MINIMIZE = 0
    MAXIMIZE = 1
