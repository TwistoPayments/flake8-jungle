import structlog

log = structlog.get_logger()

log.info("Foo {}".format("bar"))


def func():
    var = 5
    log.debug("Bar foo", {"a": var})


def func2():
    var = 5
    log.error("func2.var", var)


def func3():
    var = 5
    log.error("Func3 var", var=var)
