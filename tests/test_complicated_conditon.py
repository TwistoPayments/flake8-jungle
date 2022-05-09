from .utils import error_code_in_result, load_fixture_file, run_check


def test_is_complicated_condition():
    code = load_fixture_file("complicated_condition.py")
    result = run_check(code)
    assert len(result) == 1
    assert error_code_in_result("JG05", result)
    assert "Complexity 7 > 5" in result[0][2]


def test_is_not_complicated_condition():
    code = load_fixture_file("simple_condition.py")
    result = run_check(code)
    assert len(result) == 0
    assert not error_code_in_result("JG05", result)
