import pytest as pytest

from flake8_jungle.rules import RuleOptions

from .utils import error_code_in_result, load_fixture_file, run_check


@pytest.mark.parametrize(
    "function_max_length, function_result",
    [(10, 1), (30, 1), (31, 0), (500, 0)],
)
def test_is_function_too_long(function_max_length: int, function_result: int):
    code = load_fixture_file("function_too_long.py")
    result = run_check(
        code, options=RuleOptions(max_function_length=function_max_length)
    )
    assert len(result) == function_result
    if function_result == 1:
        assert error_code_in_result("JG06", result)


def test_is_not_function_too_long():
    code = load_fixture_file("function_length_ok.py")
    result = run_check(code)
    assert len(result) == 0
    assert not error_code_in_result("JG06", result)
