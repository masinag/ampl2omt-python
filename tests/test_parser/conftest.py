import pytest

from nl_omt.parsing.builder import ProblemBuilder
from nl_omt.parsing.nlparser import NLParser
from nl_omt.term.manager import TermManager


@pytest.fixture(scope='module')
def manager():
    return TermManager()


@pytest.fixture(scope='module')
def parser(manager):
    return NLParser(manager)


@pytest.fixture(scope='function')
def builder():
    return ProblemBuilder()
