from django.db.models import Model


class StrBeforeFieldModel2(Model):
    random_property = "foo"
    random_property2 = "foo"
    random_property3 = "foo"
    random_property4 = "foo"
    random_property5 = "foo"
    random_property6 = "foo"
    random_property7 = "foo"
    random_property8 = "foo"
    random_property9 = "foo"
    random_property10 = "foo"
    random_property11 = "foo"
    random_property12 = "foo"
    random_property13 = "foo"

    class Meta:
        verbose_name = "test"
        verbose_name_plural = "tests"

    def __str__(self):
        return "Something!"

    def save(self, **kwargs):
        super(StrBeforeFieldModel2, self).save(**kwargs)

    def get_absolute_url(self):
        return "http://%s" % self

    def my_method(self):
        pass

    @property
    def random_property(self):
        return "%s" % self

    def foo(self, a=5):
        for _ in range(10):
            a += 1
        print("foo")

        if a == 5:
            return "abc"
        if a == 6:
            return "abc"
        if a == 7:
            return "abc"

        for _ in range(10):
            a += 1
        print("foo")

    def bar(self, a=5):
        for _ in range(10):
            a += 1
        print("bar")

        if a == 5:
            return "abc"
        if a == 6:
            return "abc"
        if a == 7:
            return "abc"

        for _ in range(10):
            a += 1
        print("bar")

    def baz(self, a=5):
        for _ in range(10):
            a += 1
        print("baz")

        if a == 5:
            return "abc"
        if a == 6:
            return "abc"
        if a == 7:
            return "abc"

        for _ in range(10):
            a += 1
        print("baz")
