from __future__ import annotations

import ast
from typing import Iterable

from .base import Issue, Rule


class JG09(Issue):
    code = "JG09"
    description = (
        "Incorrect logging format, please use the following syntax: "
        'logging.{level}("MESSAGE %(arg1)s", {{"arg1": "value1"}}).'
    )


class LoggingFormatRule(Rule[ast.Call]):
    """Rule which forbids usage of `.format()`, `f-string` and `% (var,)` usage
    in logging calls.

    The only allowed forms are:

        logging.info("Request %s did not succed.", request.correlation_id)
        logging.info("Request %(id)s did not succed.", {"id": request.correlation_id})
    """

    LOGGING_CALLS: set[str] = {"log", "logger", "logging"}

    def is_logging_call(self, node: ast.Call) -> bool:
        return (
            isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in self.LOGGING_CALLS
        )

    def is_incorrect_format(self, node: ast.Call) -> bool:
        if len(node.args) == 1:
            not_allowed = (
                ast.Call,  # represents "{}".format("string")
                ast.BinOp,  # represents "%s" % ("string",)
                ast.JoinedStr,  # represents f"{variable}"
            )
            if isinstance(node.args[0], not_allowed):
                return True
        return False

    def run(self, node: ast.Call) -> Iterable[Issue]:
        issues = []

        if self.is_logging_call(node) and self.is_incorrect_format(node):
            issues.append(
                JG09(
                    lineno=node.lineno,
                    col=node.col_offset,
                    parameters={"level": node.func.attr},  # type: ignore
                )
            )

        return issues
