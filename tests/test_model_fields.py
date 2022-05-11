import pytest

from flake8_jungle.rules.jg03_model_fields import NOT_NULL_TRUE_FIELDS

from .utils import error_code_in_result, run_check


@pytest.mark.parametrize("field_type", NOT_NULL_TRUE_FIELDS)
def test_not_null_fields_fails(field_type):
    code = "field = models.{}(null=True)".format(field_type)
    result = run_check(code)
    assert error_code_in_result("JG03", result)


@pytest.mark.parametrize("field_type", NOT_NULL_TRUE_FIELDS)
def test_not_null_fields_success(field_type):
    code = "field = models.{}()".format(field_type)
    result = run_check(code)
    assert not error_code_in_result("JG03", result)


@pytest.mark.parametrize("field_type", NOT_NULL_TRUE_FIELDS)
def test_null_fields_with_unique_true_success(field_type):
    code = "field = models.{}(null=True, unique=True, blank=True)".format(field_type)
    result = run_check(code)
    assert not error_code_in_result("JG03", result)


@pytest.mark.parametrize("field_type", NOT_NULL_TRUE_FIELDS)
def test_blank_as_an_expression_does_not_raise_an_error(field_type):
    code = "field = models.{}(null=True, blank=not settings.SETTING)".format(field_type)
    result = run_check(code)
    assert error_code_in_result("JG03", result)
