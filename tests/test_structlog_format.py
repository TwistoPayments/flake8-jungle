from .utils import error_code_in_result, load_fixture_file, run_check


def test_is_not_structlog_format():
    code = load_fixture_file("bad_structlog_format.py")
    result = run_check(code, rule_id="JG11")
    assert len(result) == 4
    assert error_code_in_result("JG11", result)


def test_is_structlog_format():
    code = load_fixture_file("good_structlog_format.py")
    result = run_check(code, rule_id="JG11")
    assert len(result) == 0
    assert not error_code_in_result("JG11", result)
