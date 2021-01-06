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


@dock(
    field1='asdf',
    class_field1='asdf',
    class_field2='asdf'
)
class MyType(object):
    """
    """

    class_field1 = 123  # Can't be introspected
    class_field2: int = 1024  # Introspectable

    @dock(
        name='asdf'
    )
    def __init__(self, name: str = 'asdf'):
        """
        asdf
        """
        self.name = name
        self.field1 = field  # Can't be introspected




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
