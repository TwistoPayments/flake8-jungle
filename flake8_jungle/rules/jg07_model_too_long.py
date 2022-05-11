from __future__ import annotations

import ast
from typing import Iterable

from .base import BaseModelRule, Issue


class JG07(Issue):
    code = "JG07"
    description = (
        "Model is too long, split it into services, selectors, or utilities. "
        "Length {found} > {allowed}."
    )


class ModelTooLongRule(BaseModelRule[ast.ClassDef]):
    """Rule limiting length (measured by lines of code) of models.

    Too long models are hard to read, hard to maintain and usually are far from
    following the Domain-Driven Design.
    """

    model_name_lookup = "Model"

    def checker_applies(self, node: ast.ClassDef) -> bool:
        for base in node.bases:
            if self.is_model_name_lookup(base) or self.is_models_name_lookup_attribute(
                base
            ):
                return True
        return False

    def run(self, node: ast.ClassDef) -> Iterable[Issue]:
        issues: list = []

        if not self.checker_applies(node) or node.end_lineno is None:
            return issues

        length = node.end_lineno - node.lineno

        if length > self.options.max_model_length:
            issues.append(
                JG07(
                    lineno=node.lineno,
                    col=node.col_offset,
                    parameters={
                        "found": length,
                        "allowed": self.options.max_model_length,
                    },
                )
            )

        return issues
