import structlog

log = structlog.get_logger()

log.info("a.b.c", d="e")


def func():
    var = 5
    log.debug("bar.foo", baz=var)


def func2():
    log.error("func2.var")


def func3():
    var = 5
    log.error("func3.var", var=var, baz="baz")
