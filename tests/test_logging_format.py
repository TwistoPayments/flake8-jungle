from .utils import error_code_in_result, load_fixture_file, run_check


def test_is_bad_logging_format():
    code = load_fixture_file("bad_logging_format.py")
    result = run_check(code)
    assert len(result) == 3
    assert error_code_in_result("JG09", result)


def test_is_not_bad_logging_format():
    code = load_fixture_file("good_logging_format.py")
    result = run_check(code)
    assert len(result) == 0
    assert not error_code_in_result("JG09", result)
