import io
import os

from nl_omt.expression.factory import NodeFactory
from nl_omt.expression.node import Node
from nl_omt.problem.objective import Objective
from nl_omt.problem.problem import NLPProblem


class NLParser:
    """
    Parser for Nonlinear Programming (NLP) problems in AMPL format (nl file).
    """

    def __init__(self, node_factory: NodeFactory):
        self.node_factory = node_factory

        self.n_vars: int = 0
        self.n_cons: int = 0
        self.n_obj: int = 0
        self.n_ranges: int = 0
        self.n_eqs: int = 0
        self.n_lns: int = 0

        self.problem_vars: dict[int, Node] = {}
        self.defined_vars: dict[int, Node] = {}

        self.cons_body: dict[int, Node] = {}
        self.obj: list[Objective] = []
        self.ranges: list[Node] = []
        self.eqs: list[Node] = []
        self.lns: list[Node] = []

    def parse_file(self, path: str) -> NLPProblem:
        """
        Parse an NLP problem from a file.

        :param path: The path to the file.
        :return: The parsed NLP problem.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        if not path.endswith(".nl"):
            raise ValueError("File is not a .nl file")

        with open(path, "r") as file:
            return self.parse_stream(file)

    def parse_string(self, string: str) -> NLPProblem:
        """
        Parse an NLP problem from a string.

        :param string: The string to parse.
        :return: The parsed NLP problem.
        """
        return self.parse_stream(io.StringIO(string))

    def parse_stream(self, stream: io.TextIOBase) -> NLPProblem:
        """
        Parse an NLP problem from a stream.

        :param stream: The stream to parse.
        :return: The parsed NLP problem.
        """
        try:
            self.parse_header(stream)
        except EOFError:
            raise ValueError("Invalid header")
        while True:
            try:
                self.parse_segment(stream)
            except EOFError:
                break

    def _next_line(self, stream: io.TextIOBase) -> str:
        line = stream.readline()
        line = line.split("#")[0]
        return line.strip()

    def parse_header(self, stream: io.TextIOBase):
        self._parse_header_first_line(stream)
        self._parse_header_second_line(stream)
        self._parse_header_third_line(stream)
        self._parse_header_fourth_line(stream)
        self._parse_header_fifth_line(stream)
        self._parse_header_sixth_line(stream)
        self._parse_header_seventh_line(stream)
        self._parse_header_eight_line(stream)
        self._parse_header_ninth_line(stream)
        self._parse_header_tenth_line(stream)

    def _parse_header_first_line(self, stream):
        line = self._next_line(stream)
        if line[0] != "g":
            raise ValueError("Unsupported format: expected file to start with 'g'")
        line = line[1:]
        try:
            parts = line.split()
            assert len(parts) == 4
            _ = list(map(int, parts))
        except (ValueError, AssertionError):
            raise ValueError("Invalid header: expected 'g<n1> <n2> <n3> <n4>'")

    def _parse_header_second_line(self, stream: io.TextIOBase):
        line = self._next_line(stream)
        try:
            n_vars, n_cons, n_obj, n_ranges, n_eqs, *n_lns = map(int, line.split())
        except ValueError:
            raise ValueError("Invalid header: expected 'n_vars n_cons n_nonlin_cons n_obj n_ranges n_eqs [n_lns]'")
        if n_lns:
            raise ValueError("Logic constraints not supported yet")
        self.n_vars = n_vars
        self.n_cons = n_cons
        self.n_obj = n_obj
        self.n_ranges = n_ranges
        self.n_eqs = n_eqs

        self._init_vars(stream)

    def _init_vars(self, stream: io.TextIOBase):
        for i in range(self.n_vars):
            self.problem_vars[i] = self.node_factory.VarReal(f"x{i + 1}")

    def _parse_header_third_line(self, stream: io.TextIOBase):
        line = self._next_line(stream)
        try:
            # nonlinear constraints, objectives
            _, _ = map(int, line.split())
        except ValueError:
            raise ValueError("Invalid header: expected 'n_nonlin_cons nonlin_obj'")

    def _parse_header_fourth_line(self, stream: io.TextIOBase):
        line = self._next_line(stream)
        try:
            # nonlinear constraints, objectives
            n_network_nonlin_cons, n_network_lin_cons = map(int, line.split())
        except ValueError:
            raise ValueError("Invalid header: expected 'n_obj_ranges n_obj_eqs'")

        if n_network_lin_cons or n_network_nonlin_cons:
            raise ValueError("Network constraints not supported yet")

    def _parse_header_fifth_line(self, stream: io.TextIOBase):
        line = self._next_line(stream)
        try:
            # nonlinear vars in constraints, objectives, both
            _, _, _ = map(int, line.split())
        except ValueError:
            raise ValueError("Invalid header: expected 'n_nonlin_vars_cons n_nonlin_vars_obj n_nonlin_vars_both'")

    def _parse_header_sixth_line(self, stream: io.TextIOBase):
        line = self._next_line(stream)
        try:
            # linear network variables; functions; arith, flags
            _, _, _, _ = map(int, line.split())
        except ValueError:
            raise ValueError("Invalid header: expected 'n_lin_vars n_funcs n_arith n_flags'")

    def _parse_header_seventh_line(self, stream: io.TextIOBase):
        line = self._next_line(stream)
        try:
            # discrete variables: binary, integer, nonlinear (b,c,o)
            dv_bin, dv_int, dv_nonlin_b, dv_nonlin_c, dv_nonlin_o = map(int, line.split())
        except ValueError:
            raise ValueError(
                "Invalid header: expected 'n_bin_vars n_int_vars n_nonlin_vars_b n_nonlin_vars_c n_nonlin_vars_o'")
        if dv_bin or dv_int or dv_nonlin_b or dv_nonlin_c or dv_nonlin_o:
            raise ValueError("Discrete variables not supported yet")

    def _parse_header_eight_line(self, stream: io.TextIOBase):
        line = self._next_line(stream)
        try:
            # nonzeros in Jacobian, gradients
            _, _ = map(int, line.split())
        except ValueError:
            raise ValueError("Invalid header: expected 'n_jac_nz n_grad_nz'")

    def _parse_header_ninth_line(self, stream: io.TextIOBase):
        line = self._next_line(stream)
        try:
            # max name lengths: constraints, variables
            _, _ = map(int, line.split())
        except ValueError:
            raise ValueError("Invalid header: expected 'max_name_len_cons max_name_len_vars'")

    def _parse_header_tenth_line(self, stream: io.TextIOBase):
        line = self._next_line(stream)
        try:
            # common exprs: b,c,o,c1,o1
            _, _, _, _, _ = map(int, line.split())
        except ValueError:
            raise ValueError(
                "Invalid header: expected 'n_common_exprs_b n_common_exprs_c n_common_exprs_o n_common_exprs_c1 n_common_exprs_o1'")

    def parse_segment(self, stream: io.TextIOBase):
        pass
