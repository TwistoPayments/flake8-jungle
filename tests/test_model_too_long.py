from flake8_jungle.rules.base import RuleOptions

from .utils import error_code_in_result, load_fixture_file, run_check


def test_is_model_too_long():
    code = load_fixture_file("model_too_long.py")
    options = RuleOptions(max_model_length=50)
    result = run_check(code, options=options)
    assert len(result) == 1
    assert error_code_in_result("JG07", result)


def test_is_not_model_too_long():
    code = load_fixture_file("model_too_long.py")
    options = RuleOptions(max_model_length=500)
    result = run_check(code, options=options)
    assert len(result) == 0
    assert not error_code_in_result("JG07", result)
