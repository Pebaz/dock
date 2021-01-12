import dock



class Parent:
    DONT = 'SHOW UP'

    def __init__(self):
        pass
    def show(self):
        ...


@dock(field1='A way to store something without actually doing anything')
class Foo(Parent):
    """
    ### Usage

    ```python
    print('asdf')
    ```
    """
    X = 'y'

    @dock
    def __init__(self):
        Parent.__init__(self)
        self.field1 = 'asdf'

    @dock()
    def hello(self):
        ...


@dock
class AnotherClass:
    """Can you see me?"""
