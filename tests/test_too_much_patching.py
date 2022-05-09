from .utils import error_code_in_result, load_fixture_file, run_check


def test_is_too_much_patching():
    code = load_fixture_file("too_much_patching.py")
    result = run_check(code)
    assert len(result) == 1
    assert error_code_in_result("JG10", result)
    assert "(5 > 3)" in result[0][2]


def test_is_not_too_much_patching():
    code = load_fixture_file("no_patching.py")
    result = run_check(code)
    assert len(result) == 0
    assert not error_code_in_result("JG09", result)
