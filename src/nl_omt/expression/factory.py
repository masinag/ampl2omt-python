from typing import Iterable, Any

from nl_omt.expression.node import Node, Kind


class NodeFactory:
    """
    Factory class for creating nodes.

    This class is used to create nodes for the expression tree.
    Nodes are cached to avoid creating duplicate nodes.
    """

    def __init__(self):
        self._cache = {}

    def create(self, kind: Kind, children: tuple[Node, ...], name: str | None, value: Any | None = None) -> Node:
        """
        Create a node.

        :param kind: The kind of the node.
        :param children: The children of the node.
        :param name: The name of the node.
        :param value: The value of the node if it is a constant node.
        :return: The created node.
        """
        key = (kind, children, name)
        if key not in self._cache:
            self._cache[key] = Node(kind, children, name)
        return self._cache[key]

    def create_constant(self, kind: Kind, value: Any) -> Node:
        return self.create(kind, tuple(), None, value)

    def create_variable(self, kind: Kind, name: str) -> Node:
        return self.create(kind, tuple(), name)

    def create_unary(self, kind: Kind, child: Node, name: str | None = None) -> Node:
        return self.create(kind, (child,), name)

    def create_binary(self, kind: Kind, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create(kind, (left, right), name)

    def create_nary(self, kind: Kind, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create(kind, tuple(children), name)

    # Unary Operators
    def Floor(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.FLOOR, child, name)

    def Ceil(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.CEIL, child, name)

    def Abs(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.ABS, child, name)

    def Neg(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.NEG, child, name)

    def Not(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.NOT, child, name)

    def Tanh(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.TANH, child, name)

    def Tan(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.TAN, child, name)

    def Sqrt(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.SQRT, child, name)

    def Sinh(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.SINH, child, name)

    def Sin(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.SIN, child, name)

    def Log10(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.LOG10, child, name)

    def Log(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.LOG, child, name)

    def Exp(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.EXP, child, name)

    def Cosh(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.COSH, child, name)

    def Cos(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.COS, child, name)

    def Atanh(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.ATANH, child, name)

    def Atan(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.ATAN, child, name)

    def Asinh(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.ASINH, child, name)

    def Asin(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.ASIN, child, name)

    def Acosh(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.ACOSH, child, name)

    def Acos(self, child: Node, name: str | None = None) -> Node:
        return self.create_unary(Kind.ACOS, child, name)

    # Binary Operators

    def Plus(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.PLUS, left, right, name)

    def Minus(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.MINUS, left, right, name)

    def Mult(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.MULT, left, right, name)

    def Div(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.DIV, left, right, name)

    def Rem(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.REM, left, right, name)

    def Pow(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.POW, left, right, name)

    def Less(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.LESS, left, right, name)

    def Or(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.OR, left, right, name)

    def And(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.AND, left, right, name)

    def Lt(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.LT, left, right, name)

    def Le(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.LE, left, right, name)

    def Eq(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.EQ, left, right, name)

    def Ge(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.GE, left, right, name)

    def Gt(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.GT, left, right, name)

    def Ne(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.NE, left, right, name)

    def Atan2(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.ATAN2, left, right, name)

    def IntDiv(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.INTDIV, left, right, name)

    def Precision(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.PRECISION, left, right, name)

    def Round(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.ROUND, left, right, name)

    def Trunc(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.TRUNC, left, right, name)

    def Iff(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.IFF, left, right, name)

    # N-ary Operators
    def Min(self, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create_nary(Kind.MIN, children, name)

    def Max(self, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create_nary(Kind.MAX, children, name)

    def Sum(self, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create_nary(Kind.SUM, children, name)

    def Count(self, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create_nary(Kind.COUNT, children, name)

    def NumberOf(self, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create_nary(Kind.NUMBEROF, children, name)

    def Numberofs(self, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create_nary(Kind.NUMBEROFS, children, name)

    def AndN(self, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create_nary(Kind.ANDN, children, name)

    def OrN(self, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create_nary(Kind.ORN, children, name)

    def AllDiff(self, children: Iterable[Node], name: str | None = None) -> Node:
        return self.create_nary(Kind.ALLDIFF, children, name)

    def If(self, then_node: Node, else_node: Node, condition_node: Node, name: str | None = None) -> Node:
        return self.create(Kind.IF, (then_node, else_node, condition_node), name)

    def Ifs(self, then_node: Node, else_node: Node, condition_nodes: Node, name: str | None = None) -> Node:
        return self.create(Kind.IFS, (then_node, else_node, condition_nodes), name)

    def Implies(self, left: Node, right: Node, name: str | None = None) -> Node:
        return self.create_binary(Kind.IMPLIES, left, right, name)

    # Constants
    def Real(self, value: float, name: str | None = None) -> Node:
        return self.create_constant(Kind.REAL, value)

    def Int(self, value: int, name: str | None = None) -> Node:
        return self.create_constant(Kind.INT, value)

    def Bool(self, value: bool, name: str | None = None) -> Node:
        return self.create_constant(Kind.BOOL, value)

    # Variables
    def VarReal(self, name: str) -> Node:
        return self.create(Kind.VAR_REAL, tuple(), name)

    def VarInt(self, name: str) -> Node:
        return self.create(Kind.VAR_INT, tuple(), name)

    def VarBool(self, name: str) -> Node:
        return self.create(Kind.VAR_BOOL, tuple(), name)
