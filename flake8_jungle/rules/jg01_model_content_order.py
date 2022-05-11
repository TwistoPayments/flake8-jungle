from __future__ import annotations

import ast
from ast import Assign, ClassDef, FunctionDef
from functools import partial
from typing import Callable, Iterable

from .base import BaseModelRule, Issue


class JG01(Issue):
    code = "JG01"
    description = (
        "The order of the model's inner classes, methods, and fields does not follow "
        "the Django Style Guide: {elem_type} should come before {before}."
    )

    def __init__(self, elem, elem_type, before):
        super().__init__(elem.lineno, elem.col_offset, None)
        self.description = self.description.format(
            elem_type=elem_type,
            before=before,
        )


def is_field_declaration(node):
    """
    Verifies that the code is of the form: `field = models.CharField()`,
    matching by the `models` string.
    """
    try:
        return node.value.func.value.id == "models"
    except AttributeError:
        return False


def is_manager_declaration(node: ast.AST) -> bool:
    return (
        isinstance(node, Assign) and getattr(node.targets[0], "id", None) == "objects"
    )


def is_meta_declaration(node):
    return isinstance(node, ClassDef) and node.name == "Meta"


def is_method(node, method_name=None):
    if method_name is None:
        return isinstance(node, FunctionDef)
    return isinstance(node, FunctionDef) and node.name == method_name


class ModelContentOrderRule(BaseModelRule[ast.ClassDef]):
    """Rule which guards the order of model's inner fields, classes, methods
    and so on.
    """

    model_name_lookup = "Model"

    FIELD_DECLARATION = "field declaration"
    MANAGER_DECLARATION = "manager declaration"
    META_CLASS = "Meta class"
    STR_METHOD = "__str__ method"
    SAVE_METHOD = "save method"
    GET_ABSOLUTE_URL_METHOD = "get_absolute_url method"
    CUSTOM_METHOD = "custom method"

    MODEL_CONTENT_TYPE_EXPECTED_ORDER: dict[str, int] = {
        FIELD_DECLARATION: 0,
        MANAGER_DECLARATION: 1,
        META_CLASS: 2,
        STR_METHOD: 3,
        SAVE_METHOD: 4,
        GET_ABSOLUTE_URL_METHOD: 5,
        CUSTOM_METHOD: 6,
    }
    CONTENT_TYPE_CHECKS: list[tuple[Callable, str]] = [
        (is_field_declaration, FIELD_DECLARATION),
        (is_manager_declaration, MANAGER_DECLARATION),
        (is_meta_declaration, META_CLASS),
        (partial(is_method, method_name="__str__"), STR_METHOD),
        (partial(is_method, method_name="save"), SAVE_METHOD),
        (partial(is_method, method_name="get_absolute_url"), GET_ABSOLUTE_URL_METHOD),
        (is_method, CUSTOM_METHOD),
    ]

    def checker_applies(self, node: ast.ClassDef) -> bool:
        for base in node.bases:
            if self.is_model_name_lookup(base) or self.is_models_name_lookup_attribute(
                base
            ):
                return True
        return False

    def run(self, node: ast.ClassDef) -> Iterable[Issue]:
        if not self.checker_applies(node):
            return []

        return self.get_issues(node)

    def get_issues(self, node: ast.ClassDef) -> Iterable[Issue]:
        elements_type_found: list = []
        for element in node.body:
            element_type = self.get_element_type(element)
            if not element_type:
                continue

            element_type_in_wrong_order = self.find_element_type_in_wrong_order(
                element_type, elements_type_found
            )
            if element_type_in_wrong_order:
                yield JG01(
                    element,
                    element_type,
                    element_type_in_wrong_order,
                )
            else:
                elements_type_found.append(element_type)

    def get_element_type(self, element: ast.AST) -> str | None:
        for check, element_type in self.CONTENT_TYPE_CHECKS:
            if check(element):
                return element_type
        return None

    def find_element_type_in_wrong_order(
        self, element_type: str, elements_type_found: list[str]
    ) -> str | None:
        current_element_type_order = self.get_expected_order(element_type)
        for element_type in elements_type_found:
            if self.get_expected_order(element_type) > current_element_type_order:
                return element_type
        return None

    def get_expected_order(self, element_type: str) -> int:
        return self.MODEL_CONTENT_TYPE_EXPECTED_ORDER.get(element_type, 0)
