# NODE KINDS
# UNARY OPERATORS
# -- arithmetic operators
from enum import Enum
from typing import Any, Iterable


class Kind(Enum):
    """
    An enumeration of the different kinds of nodes in an expression graph.
    """
    # UNARY OPERATORS
    # -- arithmetic operators
    FLOOR = 13
    CEIL = 14
    ABS = 15
    NEG = 16  # unary minus
    # -- logical operators
    NOT = 34
    # -- arithmetic operators
    TANH = 37
    TAN = 38
    SQRT = 39
    SINH = 40
    SIN = 41
    LOG10 = 42
    LOG = 43
    EXP = 44
    COSH = 45
    COS = 46
    ATANH = 47
    ATAN = 49
    ASINH = 50
    ASIN = 51
    ACOSH = 52
    ACOS = 53

    # BINARY OPERATORS
    # -- arithmetic operators
    PLUS = 0
    MINUS = 1
    MULT = 2
    DIV = 3
    REM = 4
    POW = 5
    LESS = 6
    # -- logical operators
    OR = 20
    AND = 21
    # -- comparison operators
    LT = 22
    LE = 23
    EQ = 24
    GE = 28
    GT = 29
    NE = 30
    # -- arithmetic operators
    ATAN2 = 48
    INTDIV = 55
    PRECISION = 56
    ROUND = 57
    TRUNC = 58
    IFF = 73

    # N-ARY OPERATORS
    MIN = 11
    MAX = 12
    SUM = 54
    COUNT = 59
    NUMBEROF = 60
    NUMBEROFS = 61
    ANDN = 70
    ORN = 71
    ALLDIFF = 74
    IF = 35
    IFS = 65
    IMPLIES = 72

    # CONSTANTS
    REAL = -1
    INT = -2
    BOOL = -3

    # VARIABLES
    VAR_REAL = -4
    VAR_INT = -5
    VAR_BOOL = -6


class Node:
    """
    A class to represent a node in an expression graph.
    """

    def __init__(self, kind: Kind, children: Iterable['Node'], name: str | None = None):
        self.kind = kind
        self.children = children
        self.name = name


class Constant(Node):
    """
    A class to represent a constant node in an expression graph.
    """

    def __init__(self, kind: Kind, value: Any):
        super().__init__(kind, tuple())
        self.value = value
