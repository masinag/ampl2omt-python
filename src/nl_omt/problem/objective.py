from nl_omt.expression.node import Node


class Objective:
    """
    A class to represent an objective.

    :param name: The name of the objective.
    :param kind: The kind of the objective (MINIMIZE or MAXIMIZE).
    :param ExpressionGraph: The expression graph.
    """

    def __init__(self, kind: int, expression_graph: Node, name: str | None = None):
        self.expression_graph = expression_graph
        self.name = name
        self.kind = kind

    def __str__(self):
        s = f"{self.name}: " if self.name is not None else ""
        return f"{s}{self.kind} {self.expression_graph}"
