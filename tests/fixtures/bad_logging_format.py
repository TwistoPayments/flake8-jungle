import logging

log = logging.getLogger("test")

log.info("Foo {}".format("bar"))


def func():
    var = 5
    log.debug(f"Bar {var}")


def func2():
    var = 5
    log.error("Bar %s" % (var,))
