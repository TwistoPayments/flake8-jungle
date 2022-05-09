import unittest
from unittest import mock
from unittest.mock import patch


class TestSomething(unittest.TestCase):
    @patch("app.scoring.get_foo")
    @unittest.patch("app.scoring.models.BarModel")
    def test_foo_bar(self, get_foo, bar_model):
        foo = "bar"

        mock.patch("app.foo.bar", return_value=5)

        with mock.patch("libs.openscoring.Openscoring.evaluate", return_value=1), patch(
            "app.something.models.order.Order.notify"
        ):
            self.create_foo(foo)
