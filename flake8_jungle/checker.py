from __future__ import annotations

import argparse
import ast
import dataclasses
from typing import Iterator

from flake8.options.manager import OptionManager

from flake8_jungle.rules import (
    ComplicatedConditionRule,
    FunctionTooLongRule,
    ImportInsideFunctionRule,
    LoggingFormatRule,
    ModelContentOrderRule,
    ModelFieldRule,
    ModelFormRule,
    ModelTooLongRule,
    Rule,
    RuleOptions,
    TooMuchPatchingRule,
    TryExceptPassRule,
)


class JungleStyleVisitor(ast.NodeVisitor):
    """
    Visit the node, and return issues.
    """

    checkers: dict[str, list[type[Rule]]] = {
        "Call": [
            ModelFieldRule,
            LoggingFormatRule,
        ],
        "ClassDef": [
            ModelFormRule,
            ModelContentOrderRule,
            ModelTooLongRule,
        ],
        "FunctionDef": [
            FunctionTooLongRule,
            ImportInsideFunctionRule,
            TooMuchPatchingRule,
        ],
        "AsyncFunctionDef": [
            FunctionTooLongRule,
            ImportInsideFunctionRule,
            TooMuchPatchingRule,
        ],
        "Try": [
            TryExceptPassRule,
        ],
        "If": [
            ComplicatedConditionRule,
        ],
    }

    def __init__(self, options: RuleOptions, *args, **kwargs) -> None:
        super(JungleStyleVisitor, self).__init__(*args, **kwargs)

        self.issues: list = []
        self.options: RuleOptions = options

    def capture_issues_visitor(self, visitor: str, node: ast.AST) -> None:
        for checker in self.checkers[visitor]:
            issues = checker(self.options).run(node)
            if issues:
                self.issues.extend(issues)
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        self.capture_issues_visitor("Call", node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.capture_issues_visitor("ClassDef", node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.capture_issues_visitor("FunctionDef", node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.capture_issues_visitor("AsyncFunctionDef", node)

    def visit_Try(self, node: ast.Try) -> None:
        self.capture_issues_visitor("Try", node)

    def visit_If(self, node: ast.If) -> None:
        self.capture_issues_visitor("If", node)


class JungleStyleChecker:
    """
    Check common Twisto Style errors
    """

    name = "flake8-twisto"
    version = "1.0.2"

    _options = None
    _option_fields = dataclasses.fields(RuleOptions)

    def __init__(self, tree: ast.AST, filename: str) -> None:
        self.tree = tree
        self.filename = filename
        self._rule_options: RuleOptions | None = None

    @property
    def options(self) -> RuleOptions:
        if self._rule_options is None:
            options_kwargs = {}
            for field in self._option_fields:
                value = getattr(self._options, field.name, None)
                if value is not None:
                    options_kwargs[field.name] = value
            self._rule_options = RuleOptions(**options_kwargs)
        return self._rule_options

    @options.setter
    def options(self, value: RuleOptions) -> None:
        self._rule_options = value

    def run(self) -> Iterator[tuple[int, int, str, type]]:
        parser = JungleStyleVisitor(RuleOptions(**vars(self.options)))
        parser.visit(self.tree)

        for issue in parser.issues:
            yield issue.lineno, issue.col, issue.message, JungleStyleChecker

    @classmethod
    def add_options(cls, parser: OptionManager) -> None:
        for field in cls._option_fields:
            parser.add_option(
                f'--{field.name.replace("_", "-")}',
                type=field.type,
                default=field.default,
                parse_from_config=True,
            )

    @classmethod
    def parse_options(cls, options: argparse.Namespace) -> None:
        cls._options = options
