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

    def run(self, node: ast.Try) -> Iterable[Issue]:
        issues = []

        for handler in node.handlers:
            if len(handler.body) == 1 and isinstance(
                handler.body[0], (ast.Pass, ast.Return)
            ):
                pass_node = handler.body[0]
                issues.append(
                    JG04(
                        lineno=pass_node.lineno,
                        col=pass_node.col_offset,
                    )
                )

        return issues
