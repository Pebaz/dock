from typing import Tuple
import dock

@dock
class ASDF:
    ...

@dock(
    short='Just a little function that does nothing at all.',
    Usage="""
    ```python
    >>> a, b, c = some_func(1, 2, 3)
    >>> a
    1
    >>> b
    2
    >>> c
    3
    ```
    """,
    b='Just something'
)
def some_func(a: int, b: int, c: ASDF) -> Tuple[int, int, int]:
    """
    Can be used if you want.

    It doesn't really matter.
    """
    return a, b, c
