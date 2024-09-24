import pytest

from nl_omt.term.manager import TermManager


@pytest.fixture(scope='module')
def mgr():
    return TermManager()
