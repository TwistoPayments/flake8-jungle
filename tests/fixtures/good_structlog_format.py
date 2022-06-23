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


def func4():
    var = 5
    msg = "func4.var"
    log.error(msg, var=var, baz="baz")


def func5():
    var = 5
    msg = "func5.var"
    log.warning(f"{msg}.something", var=var, baz="baz")


def func6():
    var = 5
    msg = "func6.var"
    log.warning("{msg}.something".format(msg=msg), var=var, baz="baz")
    return msg


def func7():
    var = 5
    log.warning(func6(), var=var, baz="baz")
