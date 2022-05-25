from __future__ import annotations

import ast
from typing import Iterable

from .base import Issue, Rule


class JG05(Issue):
    code = "JG05"
    description = (
        "Condition is too complex which makes it impossible to understand. "
        "Complexity {found} > {allowed}."
    )


class ComplicatedConditionRule(Rule[ast.If]):
    """Rule limitting complexity of IF conditions.

    Too complex conditions are harder to read and can introduce bugs.
    """

    #: Weight of complexity for each op. Default is 1.
    CMP_WEIGHTS: dict[type[ast.cmpop], int] = {
        ast.NotEq: 2,
        ast.In: 2,
        ast.NotIn: 2,
    }

    def _calculate_compare_complexity(self, cmp: ast.Compare) -> int:
        return sum(self.CMP_WEIGHTS.get(type(op), 1) for op in cmp.ops)

    def _calculate_complexity(self, test: ast.expr) -> int:
        complexity = 1
        if isinstance(test, ast.UnaryOp):
            complexity += self._calculate_complexity(test.operand)
        elif isinstance(test, ast.BoolOp):
            for value in test.values:
                complexity += self._calculate_complexity(value)
        elif isinstance(test, ast.NamedExpr):
            complexity += self._calculate_complexity(test.value)
        elif isinstance(test, ast.Compare):
            complexity += self._calculate_compare_complexity(test)
        return complexity

    def run(self, node: ast.If) -> Iterable[Issue]:
        issues = []
        complexity = self._calculate_complexity(node.test)

        if complexity > self.options.max_condition_complexity:
            issues.append(
                JG05(
                    lineno=node.lineno,
                    col=node.col_offset,
                    parameters={
                        "found": complexity,
                        "allowed": self.options.max_condition_complexity,
                    },
                )
            )

        return issues
