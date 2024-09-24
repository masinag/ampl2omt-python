import pytest

from ampl2omt.term.manager import TermManager


@pytest.fixture(scope='module')
def mgr():
    return TermManager()
