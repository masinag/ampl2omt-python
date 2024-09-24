from dataclasses import dataclass

from ampl2omt.term.term import Term


@dataclass
class Objective:
    """
    A class to represent an objective.

    :param kind: The kind of the objective (MINIMIZE or MAXIMIZE).
    :param term: The term to be minimized or maximized.
    """
    kind: int
    term: Term

    MINIMIZE = 0
    MAXIMIZE = 1
