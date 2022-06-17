import ast
import os

from flake8_jungle import JungleStyleChecker
from flake8_jungle.rules import RuleOptions


def run_check(code, options: RuleOptions = None, rule_id: str = None):
    tree = ast.parse(code)
    checker = JungleStyleChecker(tree, None)
    checker.options = options
    return [
        issue
        for issue in checker.run()
        if rule_id is None or issue[2].startswith(f"{rule_id} ")
    ]


def load_fixture_file(filename):
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    return open(path).read()


def error_code_in_result(error_code, result):
    """
    Assert that a specific error_code is into the results

    :param error_code:
    :param result:
    :return:
    """
    for element in result:
        if error_code in element[2]:
            return True
    return False
