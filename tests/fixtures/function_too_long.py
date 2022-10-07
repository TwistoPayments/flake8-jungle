def foo(a=5):
    """Function for testing purpose

    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dignissim egestas ligula in porta.
    Nulla molestie neque vel tortor pellentesque lacinia. Phasellus eget malesuada lorem. Aliquam sollicitudin nisl
    urna, sit amet ullamcorper ex tincidunt at. Donec pretium arcu sed turpis gravida pellentesque. Aenean fringilla
    nisl et tempus imperdiet. Curabitur ut velit eu arcu gravida ultricies. Maecenas eget consequat quam.

    :param a: random int input
    :return: random useful string
    """
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
