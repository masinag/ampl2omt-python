from typing import Iterable

from nl_omt.expression.node import Node
from nl_omt.problem.objective import Objective

Constraint = Node


class NLPProblem:
    def __init__(self,
                 objective: Objective | None = None,
                 constraints: Iterable[Constraint] | None = None
                 ):
        self.objective = objective
        if constraints is None:
            constraints = []
        self.constraints = constraints
