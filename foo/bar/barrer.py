import dock

@dock
def asdf():
    "Just another place to put documentation."

@dock(
    name='The name to greet.',
    short='Whatever?',
    Usage='''
    ```python
    >>> print("Hello World!")
    >>> for i in range(100):
    ...     print(i ** 2)
    ```
    '''
)
def asdf2(name: str, age: int, alive: bool):
    """
    This is a longer description.
    """
