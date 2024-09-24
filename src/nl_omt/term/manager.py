from typing import Iterable, Any

from nl_omt.term.term import Term, TermType
from nl_omt.term.types import FLOOR, CEIL, ABS, NEG, TANH, TAN, SQRT, SINH, SIN, LOG10, LOG, EXP, COSH, COS, \
    ATANH, ATAN, ASINH, ASIN, ACOSH, ACOS, PLUS, MINUS, MULT, DIV, REM, POW, ATAN2, INTDIV, PRECISION, ROUND, TRUNC, \
    NOT, OR, AND, IF, IFS, IMPLIES, IFF, ANDN, ORN, LT, LE, EQ, GE, GT, NE, MIN, MAX, SUM, COUNT, NUMBEROF, NUMBEROFS, \
    ALLDIFF, REAL, INT, BOOL, VAR_REAL, VAR_INT, VAR_BOOL, LESS


class TermManager:
    """
    Manager for creating terms for the expression tree.

    This class is used to create terms for the expression tree.
    Nodes are cached to avoid creating duplicate terms.
    """

    def __init__(self):
        self._cache = {}
        term_types: list[TermType] = [
            # --- Arithmetic operators
            # ------ Unary operators
            TermType(FLOOR, "floor", 1),
            TermType(CEIL, "ceil", 1),
            TermType(ABS, "abs", 1),
            TermType(NEG, "-", 1),
            TermType(TANH, "tanh", 1),
            TermType(TAN, "tan", 1),
            TermType(SQRT, "sqrt", 1),
            TermType(SINH, "sinh", 1),
            TermType(SIN, "sin", 1),
            TermType(LOG10, "log10", 1),
            TermType(LOG, "log", 1),
            TermType(EXP, "exp", 1),
            TermType(COSH, "cosh", 1),
            TermType(COS, "cos", 1),
            TermType(ATANH, "atanh", 1),
            TermType(ATAN, "atan", 1),
            TermType(ASINH, "asinh", 1),
            TermType(ASIN, "asin", 1),
            TermType(ACOSH, "acosh", 1),
            TermType(ACOS, "acos", 1),
            # ------ Binary operators
            TermType(PLUS, "+", 2),
            TermType(MINUS, "-", 2),
            TermType(MULT, "*", 2),
            TermType(DIV, "/", 2),
            TermType(REM, "rem", 2),
            TermType(POW, "pow", 2),
            # TermType(LESS, "less", 2), -- max(0, a-b) -- NOT supported by SMTLIB
            TermType(ATAN2, "atan2", 2),
            TermType(INTDIV, "intdiv", 2),
            TermType(PRECISION, "precision", 2),
            TermType(ROUND, "round", 2),
            TermType(TRUNC, "trunc", 2),
            # --- Logical operators
            # ------ Unary operators
            TermType(NOT, "not", 1),
            # ------ Binary operators
            TermType(OR, "or", 2),
            TermType(AND, "and", 2),
            TermType(IF, "if", 3),
            TermType(IFS, "ifs", 3),
            TermType(IMPLIES, "implies", 2),
            TermType(IFF, "iff", 2),

            # ------ N-ary operators
            TermType(ANDN, "andn", TermType.NARY),
            TermType(ORN, "orn", TermType.NARY),
            # --- Comparison operators
            # ------ Binary operators
            TermType(LT, "<", 2),
            TermType(LE, "<=", 2),
            TermType(EQ, "=", 2),
            TermType(GE, ">=", 2),
            TermType(GT, ">", 2),
            TermType(NE, "!=", 2),
            # --- N-ary operators
            TermType(MIN, "min", TermType.NARY),
            TermType(MAX, "max", TermType.NARY),
            TermType(SUM, "sum", TermType.NARY),
            TermType(COUNT, "count", TermType.NARY),
            TermType(NUMBEROF, "numberof", TermType.NARY),
            TermType(NUMBEROFS, "numberofs", TermType.NARY),
            TermType(ALLDIFF, "alldiff", TermType.NARY),
            # --- Constants
            TermType(REAL, "real", 0),
            TermType(INT, "int", 0),
            TermType(BOOL, "bool", 0),
            # --- Variables
            TermType(VAR_REAL, "var_real", 0),
            TermType(VAR_INT, "var_int", 0),
            TermType(VAR_BOOL, "var_bool", 0),
        ]
        self._term_types = {term_type.id: term_type for term_type in term_types}

    def term_type(self, id: int) -> TermType:
        if id not in self._term_types:
            raise ValueError(f"Term type with id {id} not known.")
        return self._term_types[id]

    def create(self, term_type: TermType, children: tuple[Term, ...], payload: Any | None = None) -> Term:
        """
        Create a term.

        :param term_type: The type of the term.
        :param children: The children of the term.
        :param payload: The payload of the term.
        :return: The created term.
        """
        key = (term_type, children, payload)
        if key not in self._cache:
            self._cache[key] = Term(term_type, children, payload)
        return self._cache[key]

    def create_constant(self, term_type: TermType, value: Any) -> Term:
        return self.create(term_type, tuple(), value)

    def create_variable(self, term_type: TermType) -> Term:
        return self.create(term_type, tuple())

    def create_unary(self, term_type: TermType, child: Term) -> Term:
        return self.create(term_type, (child,))

    def create_binary(self, term_type: TermType, left: Term, right: Term) -> Term:
        return self.create(term_type, (left, right))

    def create_nary(self, term_type: TermType, children: Iterable[Term]) -> Term:
        return self.create(term_type, tuple(children))

    # Unary Operators
    def Floor(self, child: Term) -> Term:
        return self.create_unary(self.term_type(FLOOR), child)

    def Ceil(self, child: Term) -> Term:
        return self.create_unary(self.term_type(CEIL), child)

    def Abs(self, child: Term) -> Term:
        return self.create_unary(self.term_type(ABS), child)

    def Neg(self, child: Term) -> Term:
        return self.create_unary(self.term_type(NEG), child)

    def Not(self, child: Term) -> Term:
        return self.create_unary(self.term_type(NOT), child)

    def Tanh(self, child: Term) -> Term:
        return self.create_unary(self.term_type(TANH), child)

    def Tan(self, child: Term) -> Term:
        return self.create_unary(self.term_type(TAN), child)

    def Sqrt(self, child: Term) -> Term:
        return self.create_unary(self.term_type(SQRT), child)

    def Sinh(self, child: Term) -> Term:
        return self.create_unary(self.term_type(SINH), child)

    def Sin(self, child: Term) -> Term:
        return self.create_unary(self.term_type(SIN), child)

    def Log10(self, child: Term) -> Term:
        return self.create_unary(self.term_type(LOG10), child)

    def Log(self, child: Term) -> Term:
        return self.create_unary(self.term_type(LOG), child)

    def Exp(self, child: Term) -> Term:
        return self.create_unary(self.term_type(EXP), child)

    def Cosh(self, child: Term) -> Term:
        return self.create_unary(self.term_type(COSH), child)

    def Cos(self, child: Term) -> Term:
        return self.create_unary(self.term_type(COS), child)

    def Atanh(self, child: Term) -> Term:
        return self.create_unary(self.term_type(ATANH), child)

    def Atan(self, child: Term) -> Term:
        return self.create_unary(self.term_type(ATAN), child)

    def Asinh(self, child: Term) -> Term:
        return self.create_unary(self.term_type(ASINH), child)

    def Asin(self, child: Term) -> Term:
        return self.create_unary(self.term_type(ASIN), child)

    def Acosh(self, child: Term) -> Term:
        return self.create_unary(self.term_type(ACOSH), child)

    def Acos(self, child: Term) -> Term:
        return self.create_unary(self.term_type(ACOS), child)

    # Binary Operators

    def Plus(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(PLUS), left, right)

    def Minus(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(MINUS), left, right)

    def Mult(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(MULT), left, right)

    def Div(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(DIV), left, right)

    def Rem(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(REM), left, right)

    def Pow(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(POW), left, right)

    def Less(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(LESS), left, right)

    def Or(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(OR), left, right)

    def And(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(AND), left, right)

    def Lt(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(LT), left, right)

    def Le(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(LE), left, right)

    def Eq(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(EQ), left, right)

    def Ge(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(GE), left, right)

    def Gt(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(GT), left, right)

    def Ne(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(NE), left, right)

    def Atan2(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(ATAN2), left, right)

    def IntDiv(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(INTDIV), left, right)

    def Precision(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(PRECISION), left, right)

    def Round(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(ROUND), left, right)

    def Trunc(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(TRUNC), left, right)

    def Iff(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(IFF), left, right)

    # N-ary Operators
    def Min(self, children: Iterable[Term]) -> Term:
        return self.create_nary(self.term_type(MIN), children)

    def Max(self, children: Iterable[Term]) -> Term:
        return self.create_nary(self.term_type(MAX), children)

    def Sum(self, children: Iterable[Term]) -> Term:
        return self.create_nary(self.term_type(SUM), children)

    def Count(self, children: Iterable[Term]) -> Term:
        return self.create_nary(self.term_type(COUNT), children)

    def NumberOf(self, children: Iterable[Term]) -> Term:
        return self.create_nary(self.term_type(NUMBEROF), children)

    def Numberofs(self, children: Iterable[Term]) -> Term:
        return self.create_nary(self.term_type(NUMBEROFS), children)

    def AndN(self, children: Iterable[Term]) -> Term:
        return self.create_nary(self.term_type(ANDN), children)

    def OrN(self, children: Iterable[Term]) -> Term:
        return self.create_nary(self.term_type(ORN), children)

    def AllDiff(self, children: Iterable[Term]) -> Term:
        return self.create_nary(self.term_type(ALLDIFF), children)

    def If(self, condition_term: Term, then_term: Term, else_term: Term) -> Term:
        return self.create(self.term_type(IF), (condition_term, then_term, else_term))

    def Ifs(self, condition_term: Term, then_term: Term, else_term: Term) -> Term:
        return self.create(self.term_type(IFS), (condition_term, then_term, else_term))

    def Implies(self, left: Term, right: Term) -> Term:
        return self.create_binary(self.term_type(IMPLIES), left, right)

    # Constants
    def Real(self, value: float) -> Term:
        return self.create_constant(self.term_type(REAL), float(value))

    def Int(self, value: int) -> Term:
        return self.create_constant(self.term_type(INT), int(value))

    def Bool(self, value: bool) -> Term:
        return self.create_constant(self.term_type(BOOL), value)

    # Variables
    def VarReal(self, name: str) -> Term:
        return self.create(self.term_type(VAR_REAL), tuple(), name)

    def VarInt(self, name: str) -> Term:
        return self.create(self.term_type(VAR_INT), tuple(), name)

    def VarBool(self, name: str) -> Term:
        return self.create(self.term_type(VAR_BOOL), tuple(), name)
