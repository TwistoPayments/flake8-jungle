class Foo:
    def test(self):
        if test := 5 > 6:
            return test

    def test2(self):
        if test := self.test and True and True:
            return test
