from nl_omt.expression.node import Node


class ConstraintsSet:
    """
    A class to represent a set of constraints for a problem.

    :param constraints: A list of constraints.
    """

    def __init__(self, constraints: list[Node]):
        self.constraints = constraints

    def __str__(self):
        return f"ConstraintsSet:\n{'\n'.join(str(c) for c in self.constraints)}"
