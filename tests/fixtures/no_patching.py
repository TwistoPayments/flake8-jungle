import unittest


class TestSomething(unittest.TestCase):
    def test_foo_bar(self):
        foo = "bar"
        self.create_foo(foo)
