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


@dock(asdf='What in the world?')
def long_name(asdf):
    ...

@dock(returns='!', raises='?', asdf='What in the world?')
def long_name2(asdf):
    ...

@dock()
def long_name3(asdf):
    ...

@dock
def long_name4(asdf: Foo):
    ...

dock(3)
dock()
