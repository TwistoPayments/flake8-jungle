import logging

log = logging.getLogger("test")

log.info("Foo %(bar)s", {"bar": 6})


def func():
    log.debug("Baz %(baz)s", {"baz": 7})
