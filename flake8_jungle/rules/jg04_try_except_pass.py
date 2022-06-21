from __future__ import annotations

import ast
from typing import Iterable

from .base import Issue, Rule


class JG04(Issue):
    code = "JG04"
    description = (
        "Exceptions should never pass silently, add logging or comment at least."
    )


class TryExceptPassRule(Rule[ast.Try]):
    """Rule forbidding silent exception handling.

    Even though silent handling is Pythonic in some cases, it can often result
    in hiding important information.
    """

    def _is_pass(self, node: ast.stmt) -> bool:
        return isinstance(node, ast.Pass)

    def _is_return_none(self, node: ast.stmt) -> bool:
        if isinstance(node, ast.Return):
            if node.value is None:
                return True
            if isinstance(node.value, ast.Constant) and node.value.value is None:
                return True
        return False

    def run(self, node: ast.Try) -> Iterable[Issue]:
        issues = []

        for handler in node.handlers:
            if len(nodes := handler.body) != 1:
                continue
            if self._is_return_none(nodes[0]) or self._is_pass(nodes[0]):
                issues.append(
                    JG04(
                        lineno=nodes[0].lineno,
                        col=nodes[0].col_offset,
                    )
                )

        return issues
