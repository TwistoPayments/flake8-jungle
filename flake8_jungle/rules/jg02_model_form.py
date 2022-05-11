from __future__ import annotations

import ast
from typing import Iterable

from .base import BaseModelRule, Issue


class JG02(Issue):
    code = "JG02"
    description = (
        "Do not use 'exclude' attribute in ModelForm, list all items "
        "explicitly in 'fields' attribute instead."
    )


class ModelFormRule(BaseModelRule[ast.ClassDef]):
    """Rule forbidding usage of 'exclude' in model forms.

    Using exclude could result in new fields being automatically public
    if new field is added to the model.
    """

    model_name_lookup = "ModelForm"

    def checker_applies(self, node: ast.ClassDef) -> bool:
        for base in node.bases:
            is_model_form = self.is_model_name_lookup(
                base
            ) or self.is_models_name_lookup_attribute(base)
            if is_model_form:
                return True
        return False

    def run(self, node: ast.ClassDef) -> Iterable[Issue]:
        """
        Captures the use of exclude in ModelForm Meta
        """
        issues: list = []

        if not self.checker_applies(node):
            return issues

        for body in node.body:
            if not isinstance(body, ast.ClassDef):
                continue
            for element in body.body:
                if not isinstance(element, ast.Assign):
                    continue
                for target in element.targets:
                    if target.id == "exclude":  # type: ignore
                        issues.append(
                            JG02(
                                lineno=node.lineno,
                                col=node.col_offset,
                            )
                        )
        return issues
