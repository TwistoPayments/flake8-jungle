from __future__ import annotations

import ast
from typing import Iterable, Union

from .base import Issue, Rule


class JG10(Issue):
    code = "JG10"
    description = (
        "Too much patching in tests ({found} > {allowed}). "
        "Consider changing your design to utilize Dependency Injection and fakes."
    )


FunctionType = Union[ast.FunctionDef, ast.AsyncFunctionDef]


class TooMuchPatchingRule(Rule[FunctionType]):
    """Rule which counts number of `unittest.patch(...)` calls in tests.

    The rule suggests different approach if patching in tests is being overused.
    There are several reasons why patching might not be the best option:

    - it may signal that the code is violating SOLID principles
    - patching makes tests too dependent on module paths, function and class names
    - patching makes tests harder to maintain
    """

    PATCH_NAMES: set[str] = {"patch"}

    def is_patch_call(self, call: ast.AST) -> bool:
        if not isinstance(call, ast.Call):
            return False

        name = None
        if isinstance(call.func, ast.Attribute):
            name = call.func.attr
        elif isinstance(call.func, ast.Name):
            name = call.func.id
        return name in self.PATCH_NAMES

    def is_test_function(self, node: FunctionType) -> bool:
        return node.name.startswith("test_")

    def is_patch_expr(self, node: ast.AST) -> bool:
        return isinstance(node, ast.Expr) and self.is_patch_call(node.value)

    def is_patch_with(self, node: ast.AST) -> bool:
        return isinstance(node, ast.With)

    def count_patch_with_items(self, items: list[ast.withitem]) -> int:
        number_of_patch_items = 0
        for item in items:
            if self.is_patch_call(item.context_expr):
                number_of_patch_items += 1
        return number_of_patch_items

    def count_number_of_patches(self, node: FunctionType) -> int:
        number_of_patch_calls = 0

        for line in node.body:
            if self.is_patch_expr(line):
                number_of_patch_calls += 1
            elif self.is_patch_with(line):
                number_of_patch_calls += self.count_patch_with_items(
                    line.items  # type: ignore
                )

        for item in node.decorator_list:
            if self.is_patch_call(item):
                number_of_patch_calls += 1

        return number_of_patch_calls

    def run(self, node: FunctionType) -> Iterable[Issue]:
        issues: list = []

        if not self.is_test_function(node):
            return issues

        number_of_patches = self.count_number_of_patches(node)
        if number_of_patches > self.options.max_patches_in_test:
            issues.append(
                JG10(
                    lineno=node.lineno,
                    col=node.col_offset,
                    parameters={
                        "found": number_of_patches,
                        "allowed": self.options.max_patches_in_test,
                    },
                )
            )

        return issues
