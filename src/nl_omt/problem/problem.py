from dataclasses import dataclass

from nl_omt.problem.objective import Objective
from nl_omt.term.term import Term


@dataclass
class NLPProblem:
    variables: list[Term]
    objectives: list[Objective]
    constraints: list[Term]
