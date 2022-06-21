def func():
    try:
        foo = 0
        bar = 1 / foo
        print(bar)
    except TypeError:
        pass
    except ZeroDivisionError:
        pass
    except KeyError:
        return
    except Exception:
        return None
    except BaseException:
        return 5  # this is ok
