import pytest

from nl_omt.writing.smtlibwriter import SmtlibWriter


@pytest.fixture
def writer():
    return SmtlibWriter()


@pytest.fixture
def x(mgr):
    return [mgr.VarReal(f"x{i}") for i in range(9)]
