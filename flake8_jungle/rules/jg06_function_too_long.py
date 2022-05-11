from __future__ import annotations

import ast
from typing import Iterable, Union

from .base import Issue, Rule


class JG06(Issue):
    code = "JG06"
    description = "Function is too long. Length {found} > {allowed}."


FunctionType = Union[ast.FunctionDef, ast.AsyncFunctionDef]


class FunctionTooLongRule(Rule[FunctionType]):
    """Rule limitting length (measured by lines of code) of functions.

    Long functions are harder to read, test and maintain.
    """

    def run(self, node: FunctionType) -> Iterable[Issue]:
        issues: list = []

        if node.end_lineno is None:
            return issues
        length = node.end_lineno - node.lineno

        if length > self.options.max_function_length:
            issues.append(
                JG06(
                    lineno=node.lineno,
                    col=node.col_offset,
                    parameters={
                        "found": length,
                        "allowed": self.options.max_function_length,
                    },
                )
            )

        return issues
