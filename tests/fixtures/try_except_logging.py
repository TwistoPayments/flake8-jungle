import logging


def func():
    try:
        foo = 0
        bar = 1 / foo
        print(bar)
    except ZeroDivisionError:
        logging.info("module.zero_devision_error")
