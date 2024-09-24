from dataclasses import dataclass

from ampl2omt.problem.objective import Objective
from ampl2omt.term.term import Term


@dataclass
class NLPProblem:
    variables: list[Term]
    objectives: list[Objective]
    constraints: list[Term]
