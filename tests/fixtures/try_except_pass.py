def func():
    try:
        foo = 0
        bar = 1 / foo
        print(bar)
    except TypeError:
        pass
    except ZeroDivisionError:
        pass
