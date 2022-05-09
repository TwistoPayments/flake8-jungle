from .utils import error_code_in_result, load_fixture_file, run_check


def test_model_form_doesnt_set_exclude_fails():
    code = load_fixture_file("model_form_exclude.py")
    result = run_check(code)
    assert error_code_in_result("JG02", result)


def test_model_form_doesnt_set_exclude_success():
    code = load_fixture_file("model_form_fields.py")
    result = run_check(code)
    assert len(result) == 0
    assert not error_code_in_result("JG02", result)
