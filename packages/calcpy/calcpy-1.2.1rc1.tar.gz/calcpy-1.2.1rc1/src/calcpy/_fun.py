from functools import wraps


def call(f, *args, **kwargs):
    """Call a callable with positional arguments and keyword arguments.

    Parameters:
        f: Callable object.
        *args: Positional arguments.
        **kwargs: Keyword arguments.

    Returns:
        Result of the callable.

    Examples:
        >>> call(range, 2, 3, 6)
        range(2, 3, 6)
    """
    return f(*args, **kwargs)


def curry(*args, **kwargs):
    """Fill arguments of a callable.

    If you want to fill positional arguments in the middle without filling argumetns in the begining,
    you can use ``prioritize()`` to move those positional parameter to the beginning,
    and then fill them using this ``curry()``.

    Parameters:
        args (tuple): Positional arguments to fill.
        kwargs (dict): Keyword arguments to fill.

    Returns:
        Callable[callable, callable]:

    Examples:
        Use as a decorator:

        >>> @curry(2, 3)
        ... def muladd(a, b, c):
        ...     return a * b + c
        >>> muladd(4)
        10

        Use as a decorator, together with ``prioritize()``:

        >>> from calcpy.fun import prioritize
        >>> @curry(2, 3)
        ... @prioritize(-2, -1)
        ... def muladd(a, b, c):
        ...     return a * b + c
        >>> muladd(4)
        14
    """
    def wrapper(f):
        @wraps(f)
        def fun(*arguments, **keywordarguments):
            return f(*args, *arguments, **kwargs, **keywordarguments)
        return fun
    return wrapper
