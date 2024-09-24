import argparse as ap

from ampl2omt.parsing.nlparser import NLParser
from ampl2omt.term.manager import TermManager
from ampl2omt.writing.smtlibwriter import SmtlibWriter


def parse_args():
    parser = ap.ArgumentParser(
        description="Convert NonLinear Programming problems from AMPL (.nl) to OMT (.smt2) format")
    parser.add_argument("input", type=str, help="Path to the input file")
    parser.add_argument("output", type=str, help="Path to the output file")
    parser.add_argument("--daggify", action="store_true", help="Use daggified terms")
    return parser.parse_args()


def main():
    args = parse_args()
    mgr = TermManager()
    parser = NLParser(mgr)
    problem = parser.parse_file(args.input)
    writer = SmtlibWriter()
    with open(args.output, "w") as f:
        f.write(writer.to_smtlib(problem, daggify=args.daggify))
