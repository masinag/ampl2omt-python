from dataclasses import dataclass
from typing import Any, Iterable


@dataclass(frozen=True)
class TermType:
    id: int
    name: str
    arity: int

    NARY = -1


@dataclass(frozen=True)
class Term:
    term_type: TermType
    children: Iterable['Term']
    payload: Any
