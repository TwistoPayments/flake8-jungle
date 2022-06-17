from __future__ import annotations

import ast
import re
from typing import Iterable, Pattern

from .base import Issue, Rule


class JG11(Issue):
    code = "JG11"
    description = (
        "Please use structlog and follow the correct logging style: "
        'logger.{level}("snake_case_message.with_dots", key="value").'
    )


class StructlogFormatRule(Rule[ast.Call]):
    """Rule which enforces correct sturctlog conventions in logger calls.

    See https://www.structlog.org/

    The rule allows the following forms:

        logger.info("payment_task.request_failed", request_id=request.id)
    """

    LOGGER_CALLS: set[str] = {"log", "logger", "logging"}
    MSG_RE: Pattern[str] = re.compile(r"^[a-z\d\._]+$")

    def is_logging_call(self, node: ast.Call) -> bool:
        return (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in self.LOGGER_CALLS
        )

    def is_incorrect_format(self, node: ast.Call) -> bool:
        if not node.args:
            return False
        if len(node.args) > 1 or not isinstance(node.args[0], ast.Constant):
            return True
        msg = node.args[0].value
        if not self.MSG_RE.match(msg):
            return True
        return False

    def run(self, node: ast.Call) -> Iterable[Issue]:
        issues = []

        if self.is_logging_call(node) and self.is_incorrect_format(node):
            issues.append(
                JG11(
                    lineno=node.lineno,
                    col=node.col_offset,
                    parameters={"level": node.func.attr},  # type: ignore
                )
            )

        return issues
