from flake8_jungle.rules import RuleOptions

from .utils import error_code_in_result, load_fixture_file, run_check


def test_is_function_too_long():
    code = load_fixture_file("function_too_long.py")
    result = run_check(code, options=RuleOptions(max_function_length=10))
    assert len(result) == 1
    assert error_code_in_result("JG06", result)


def test_is_not_function_too_long():
    code = load_fixture_file("function_length_ok.py")
    result = run_check(code)
    assert len(result) == 0
    assert not error_code_in_result("JG06", result)
