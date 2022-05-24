from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Generic, Iterable, TypeVar


class Issue:
    """
    Abstract class for issues.
    """

    code = ""
    description = ""

    def __init__(
        self, lineno: int, col: int, parameters: dict[str, Any] = None
    ) -> None:
        self.parameters = {} if parameters is None else parameters
        self.col = col
        self.lineno = lineno

    @property
    def message(self) -> str:
        """
        Return issue message.
        """
        message = self.description.format(**self.parameters)
        return f"{self.code} {message}"


@dataclass
class RuleOptions:
    """Configuration options for flake8 rules."""

    max_model_length: int = 500
    max_function_length: int = 50
    max_condition_complexity: int = 8
    max_patches_in_test: int = 3


ASTType = TypeVar("ASTType", bound=ast.AST)


class Rule(Generic[ASTType]):
    """
    Abstract class for flake8 rules.
    """

    def __init__(self, options: RuleOptions) -> None:
        self.options = options

    @staticmethod
    def get_call_name(node: ast.Call) -> str | None:
        """
        Return call name for the given node.
        """
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        elif isinstance(node.func, ast.Name):
            return node.func.id
        return None

    def run(self, node: ASTType) -> Iterable[Issue]:
        """
        Method that runs the checks and returns the issues.
        """
        return NotImplementedError  # type: ignore


class BaseModelRule(Rule[ASTType]):
    """
    Base class for checkers that must lookup for Model like nodes.
    """

    model_name_lookup = ""

    @staticmethod
    def _is_abstract_and_set_to_true(element: ast.stmt) -> bool:
        return (
            isinstance(element, ast.Assign)
            and any(
                target.id == "abstract"
                for target in element.targets
                if isinstance(target, ast.Name)
            )
            and isinstance(element.value, ast.NameConstant)
            and element.value.value is True
        )

    def is_abstract_model(self, base: ast.expr) -> bool:
        """
        Return True if AST node has a Meta class with abstract = True.
        """
        if not hasattr(base, "body"):
            return False

        # look for "class Meta"
        for element in base.body:  # type: ignore
            if isinstance(element, ast.ClassDef) and element.name == "Meta":
                # look for "abstract = True"
                for inner_element in element.body:
                    if self._is_abstract_and_set_to_true(inner_element):
                        return True
        return False

    def is_model_name_lookup(self, base: ast.expr) -> bool:
        """
        Return True if class is defined as the respective model name lookup declaration
        """
        return isinstance(base, ast.Name) and base.id == self.model_name_lookup

    def is_models_name_lookup_attribute(self, base: ast.expr) -> bool:
        """
        Return True if class is defined as the respective model name lookup declaration
        """
        return (
            isinstance(base, ast.Attribute)
            and isinstance(base.value, ast.Name)
            and base.value.id == "models"
            and base.attr == self.model_name_lookup
        )
