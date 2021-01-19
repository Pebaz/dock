from typing import Tuple
import dock

@dock(
    Usage="""
    >>> a, b, c = some_func(1, 2, 3)
    >>> a
    1
    >>> b
    2
    >>> c
    3
    """
)
def some_func(a: int, b: int, c: int) -> Tuple[int, int, int]:
    return a, b, c
