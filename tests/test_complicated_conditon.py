import ast

import pytest

from flake8_jungle.rules import ComplicatedConditionRule, RuleOptions

from .utils import error_code_in_result, load_fixture_file, run_check


def test_is_complicated_condition():
    code = load_fixture_file("complicated_condition.py")
    result = run_check(code)
    assert len(result) == 1
    assert error_code_in_result("JG05", result)
    assert "Complexity 9 > 8" in result[0][2]


def test_is_not_complicated_condition():
    code = load_fixture_file("simple_condition.py")
    result = run_check(code)
    assert len(result) == 0
    assert not error_code_in_result("JG05", result)


@pytest.mark.parametrize(
    "condition, complexity",
    [
        ("a", 1),
        ("not a", 2),
        ("a and b", 3),
        ("a and b and c", 4),
        ("a and b and not c", 5),
        ("not a and not b and not c", 7),
        ("a in [1, 2]", 3),
        ("a not in [1, 2]", 3),
        ("a not in [1, 2] and b not in [3, 4]", 7),
        ("a == b", 2),
        ("a != b", 3),
        ("a > b >= c", 3),
        ("a > b >= c > d", 4),
        ("a > b >= c > d != e", 6),
        ("not (a and b in (1, 2) or not c)", 9),
    ],
)
def test_complexity_evaluation(condition, complexity):
    rule = ComplicatedConditionRule(RuleOptions())
    ast_test = ast.parse(f"if {condition}: pass").body[0].test
    assert rule._calculate_complexity(ast_test) == complexity
