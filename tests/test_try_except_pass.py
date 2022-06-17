from .utils import error_code_in_result, load_fixture_file, run_check


def test_is_try_except_pass():
    code = load_fixture_file("try_except_pass.py")
    result = run_check(code, rule_id="JG04")
    assert len(result) == 4
    assert error_code_in_result("JG04", result)


def test_is_not_try_except_pass():
    code = load_fixture_file("try_except_logging.py")
    result = run_check(code, rule_id="JG04")
    assert len(result) == 0
    assert not error_code_in_result("JG04", result)
