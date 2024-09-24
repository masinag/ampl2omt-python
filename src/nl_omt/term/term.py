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
    children: tuple['Term']
    payload: Any


def topo_sort(term: Term) -> Iterable[Term]:
    stack = [term]
    visited = set()
    while stack:
        node = stack[-1]
        if node in visited:
            stack.pop()
            yield node
        else:
            visited.add(node)
            stack.extend(reversed(node.children))
