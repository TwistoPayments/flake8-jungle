from __future__ import annotations

import ast
from typing import Iterable, Union

from .base import Issue, Rule


class JG08(Issue):
    code = "JG08"
    description = (
        "Function or method contains local imports, which should be mostly avoided. "
        "If you are trying to fix curcular dependency issues, the design probably "
        "has some flaws, you should consider refactoring instead."
    )


FunctionType = Union[ast.FunctionDef, ast.AsyncFunctionDef]


class ImportInsideFunctionRule(Rule[FunctionType]):
    """Rule forbidding imports inside functions.

    This can signal bad design and should not be overused.
    """

    def run(self, node: FunctionType) -> Iterable[Issue]:
        issues = []
        contains_import = False

        for line in node.body:
            if isinstance(line, (ast.Import, ast.ImportFrom)):
                contains_import = True
                break

        if contains_import:
            issues.append(
                JG08(
                    lineno=node.lineno,
                    col=node.col_offset,
                )
            )

        return issues
