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


def func5():
    var = 5
    msg = "func5.var"
    log.warning(f"{msg}.SOMETHING", var=var, baz="baz")


def func6():
    var = 5
    msg = "func6.var"
    log.warning("BAD_FORMAT.{msg}.something".format(msg=msg), var=var, baz="baz")
    return msg
