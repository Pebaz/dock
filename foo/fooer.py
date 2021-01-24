"""
*Module-level docstring.*

It can be multi-line, and contain copyright notices, etc.
"""

import dock

@dock
def asdf():
    "A function that does something that could work if it didn't."


@dock(
    other='Something',
    other2='Somethine else',
    other3='Yet another one'
)
class ClassOne:
    """
    ### Usage

    ```python
    >>> print('Hello World!')
    >>> for i in range(100):
    ...     print(i)
    ```

    You can [click this](http://www.google.com)
    """

    @dock
    def look(self):
        "Something looking"

    @dock
    class InnerOne:
        @dock
        def look_innerone(self):
            ...

@dock(raises='Something that you don\'t want to happen')
def bar():
    "A function that does something that could work if it didn't."

@dock(
    asdf='What in the world?',
    Section1='''
    This is a long section
    with multiple lines.
    ''',
    Section2='Shorter section'
)
def long_name(asdf):
    """
    First line is a short description.

    Lorem ipsum, or lipsum as it is sometimes known, is dummy text used in
    laying out print, graphic or web designs. The passage is attributed to an
    unknown typesetter in the 15th century who is thought to have scrambled
    parts of Cicero's De Finibus Bonorum et Malorum for use in a type
    """
