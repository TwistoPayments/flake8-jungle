from .utils import error_code_in_result, load_fixture_file, run_check


def test_is_import_inside_function():
    code = load_fixture_file("import_inside_function.py")
    result = run_check(code)
    assert len(result) == 2
    assert error_code_in_result("JG08", result)


def test_is_not_import_inside_function():
    code = load_fixture_file("import_outside_function.py")
    result = run_check(code)
    assert len(result) == 0
    assert not error_code_in_result("JG08", result)
