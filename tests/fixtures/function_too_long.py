def foo(a=5):
    for _ in range(10):
        a += 1
    print("bar")

    if a == 5:
        return "abc"
    if a == 6:
        return "abc"
    if a == 7:
        return "abc"

    if a == 8:
        return "abc"
    if a == 1:
        return "abc"
    if a == 2:
        return "abc"
    if a == 3:
        return "abc"

    for _ in range(10):
        a += 1
    for _ in range(10):
        a += 1
    for _ in range(10):
        a += 1
    for _ in range(10):
        a += 1
    for _ in range(10):
        a += 1
    print("bar")
