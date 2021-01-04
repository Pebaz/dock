import sys  # Make sure this gets ingnored in output file


@dock(  # Says "include this function in the generated docs"
    age='Gets returned without any processing',
    returns='The same thing that was passed in',
    raises=None
)
def function_name(age: int) -> int:
    """
    Short description of function.

    Longer description of function.
    Longer description of function.
    Longer description of function.

    #### Usage

    ```python
    # Full markdown support
    a = function_name(100)
    print(a)
    ```
    """


@dock.args(age='Gets returned without any processing')
@dock.returns('The same thing that was passed in')
@dock.raises(None)
def function_name(age: int) -> int:
    """
    Short description of function.

    Longer description of function.
    Longer description of function.
    Longer description of function.

    #### Usage

    ```python
    # Full markdown support
    a = function_name(100)
    print(a)
    ```
    """
