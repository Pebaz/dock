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
    def __init__(self):
        Parent.__init__(self)
        self.field1 = 'asdf'

    def hello(self):
        ...
