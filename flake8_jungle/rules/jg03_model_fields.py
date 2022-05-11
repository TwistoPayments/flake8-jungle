from __future__ import annotations

import ast
from typing import Iterable

from .base import Issue, Rule

NOT_NULL_TRUE_FIELDS = [
    "CharField",
    "TextField",
    "SlugField",
    "EmailField",
    "FilePathField",
    "URLField",
]


class JG03(Issue):
    code = "JG03"
    description = "Avoid using null=True on string-based fields such as {field}."


class ModelFieldRule(Rule[ast.Call]):
    """Rule forbidding null=True on string-based fields.

    Read Django documentation:
    https://docs.djangoproject.com/en/4.0/ref/models/fields/#null
    """

    def run(self, node: ast.Call) -> Iterable[Issue]:
        issues: list = []

        call_name = self.get_call_name(node)
        if call_name not in NOT_NULL_TRUE_FIELDS:
            return issues

        found_null_true = False
        found_unique_true = False
        found_blank_true = False
        for keyword in node.keywords:
            if keyword.arg == "null" and getattr(keyword.value, "value", False) is True:
                found_null_true = True

            if (
                keyword.arg == "unique"
                and getattr(keyword.value, "value", False) is True
            ):
                found_unique_true = True

            if (
                keyword.arg == "blank"
                and getattr(keyword.value, "value", False) is True
            ):
                found_blank_true = True

            # consider exception for the rule when unique=True and blank=True
            if found_blank_true and found_unique_true:
                return issues

        if found_null_true:
            issues.append(
                JG03(
                    lineno=node.lineno,
                    col=node.col_offset,
                    parameters={"field": call_name},
                )
            )
        return issues
