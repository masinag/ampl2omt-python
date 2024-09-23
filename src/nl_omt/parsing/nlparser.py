import io
import os

from nl_omt.parsing.builder import ProblemBuilder
from nl_omt.parsing.stream import LineStream
from nl_omt.problem.problem import NLPProblem
from nl_omt.term.manager import TermManager
from nl_omt.term.term import Term


class NLParser:
    """
    Parser for Nonlinear Programming (NLP) problems in AMPL format (nl file).
    """

    def __init__(self, term_manager: TermManager):
        self.term_manager = term_manager

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
        problem_builder = ProblemBuilder()
        line_stream = LineStream(stream)
        try:
            self.parse_header(line_stream, problem_builder)
        except EOFError:
            raise ValueError("Invalid header")
        while True:
            try:
                self.parse_segment(line_stream, problem_builder)
            except EOFError:
                break

        self.build_problem()

    def build_problem(self) -> NLPProblem:
        raise NotImplementedError("TODO: Implement me!")

    def parse_header(self, line_stream: LineStream, problem_builder: ProblemBuilder) -> None:
        # line 1
        line = line_stream.next_line()
        if line[0] != "g":
            raise ValueError("Unsupported format: expected file to start with 'g'")
        line = line[1:]
        line_stream.parse_ints(4, line)
        # line 2
        n_vars, n_cons, n_obj, n_ranges, n_eqs, *n_lns = line_stream.next_ints(6, n_opt=1)
        if n_lns:
            raise ValueError("Logic constraints not supported yet")
        problem_builder \
            .with_n_vars(n_vars) \
            .with_n_cons(n_cons) \
            .with_n_obj(n_obj) \
            .with_n_ranges(n_ranges) \
            .with_n_eqs(n_eqs)
        for i in range(n_vars):
            problem_builder.with_problem_var(i, self.term_manager.VarReal(f"x{i}"))
        # nonlinear constraints, objectives
        line_stream.next_ints(2)
        # network constraints: nonlinear, linear
        line_stream.next_ints(2)
        # nonlinear vars in constraints, objectives, both
        line_stream.next_ints(3)
        # linear network variables; functions; arith, flags
        line_stream.next_ints(4)
        # discrete variables: binary, integer, nonlinear (b,c,o)
        dv_bin, dv_int, dv_nonlin_b, dv_nonlin_c, dv_nonlin_o = line_stream.next_ints(5)
        if dv_bin or dv_int or dv_nonlin_b or dv_nonlin_c or dv_nonlin_o:
            raise ValueError("Discrete variables not supported yet")
        # nonzeros in Jacobian, gradients
        line_stream.next_ints(2)
        # max name lengths: constraints, variables
        line_stream.next_ints(2)
        # common exprs: b,c,o,c1,o1
        line_stream.next_ints(5)

    def parse_segment(self, line_stream: LineStream, problem_builder: ProblemBuilder) -> None:
        line = line_stream.next_line()
        # split first character from the rest of the line
        kind, line = line[0], line[1:]
        match kind:
            case "F":
                self.parse_imported_function_segment(line, line_stream, problem_builder)
            case "S":
                self.parse_suffix_segment(line, line_stream, problem_builder)
            case "V":
                self.parse_definition_segment(line, line_stream, problem_builder)
            case "C":
                self.parse_cons_body_segment(line, line_stream, problem_builder)

    def parse_imported_function_segment(self, line: str, line_stream: LineStream, problem_builder: ProblemBuilder):
        raise NotImplementedError("Imported functions not supported yet")

    def parse_suffix_segment(self, line: str, line_stream: LineStream, problem_builder: ProblemBuilder):
        raise NotImplementedError("Suffixes not supported yet")

    def parse_definition_segment(self, line: str, line_stream: LineStream, problem_builder: ProblemBuilder):
        i, j, k = line_stream.parse_ints(3, line)
        terms: list[Term] = []
        for _ in range(j):
            terms.append(self.parse_linear_term(line_stream, problem_builder))
        terms.append(self.parse_expression(line_stream, problem_builder))
        expr = self.term_manager.Sum(terms) if len(terms) > 1 else terms[0]
        problem_builder.with_definition(i, expr)

    def parse_linear_term(self, line_stream: LineStream, problem_builder: ProblemBuilder) -> Term:
        line = line_stream.next_line()
        try:
            p, c = line.split()
            p = int(p)
            c = float(c)
        except ValueError:
            raise ValueError("Invalid linear term: expected 'i j'")
        return self.term_manager.Mult(problem_builder.get_problem_var(p), self.term_manager.Real(c))

    def parse_expression(self, line_stream: LineStream, problem_builder: ProblemBuilder) -> Term:
        line = line_stream.next_line()
        kind, line = line[0], line[1:]
        match kind:
            case "n":
                return self.parse_expr_real_constant(line)
            case "v":
                return self.parse_expr_var(line, line_stream, problem_builder)
            case "f":
                return self.parse_expr_function(line)
            case "o":
                return self.parse_expr_operator(line, line_stream, problem_builder)

    def parse_expr_real_constant(self, line: str) -> Term:
        try:
            value = float(line)
        except ValueError:
            raise ValueError("Invalid real constant")
        return self.term_manager.Real(value)

    def parse_expr_var(self, line: str, line_stream: LineStream, problem_builder: ProblemBuilder) -> Term:
        i, = line_stream.parse_ints(1, line)
        if problem_builder.is_problem_var(i):
            return problem_builder.get_problem_var(i)
        return problem_builder.get_definition(i)

    def parse_expr_function(self, line: str) -> Term:
        raise NotImplementedError("Functions not supported yet")

    def parse_expr_operator(self, line: str, line_stream: LineStream, problem_builder: ProblemBuilder) -> Term:
        term_type, = line_stream.parse_ints(1, line)

        op = self.term_manager.term_type(term_type)
        arity = op.arity
        if arity == op.NARY:
            arity, = line_stream.next_ints(1)
        children = tuple(self.parse_expression(line_stream, problem_builder) for _ in range(arity))
        return self.term_manager.create(op, children)

    def parse_cons_body_segment(self, line: str, line_stream: LineStream, problem_builder: ProblemBuilder) -> None:
        i, = line_stream.parse_ints(1, line)
        expr = self.parse_expression(line_stream, problem_builder)
        problem_builder.with_cons_body(i, expr)
