<p align=center>
    <img src="misc/Dock.png" width=60% alt="Dock Logo: Deliberate Documentation">
</p>

# dock - *deliberate documentation*

Simple to use documentation generator

## Usage

```python
import dock  # Can't get any simpler

@dock  # No need to even call it
def foo():  # <- This function lacks a return type, so it's assumed to be None
    """
    This text will be included in the generated documentation.
    """

@dock()  # No need to pass arguments
def bar():
    "Will be included in the generated documentation."

# But if you do that's ok too
@dock(
    arg1='An integer you must pass',
    arg2='A string you must pass',
    arg3='A list of integers you must pass',
    returns='An integer',
    raises=None  # Implied, no need to pass if no exceptions are raised
)
def baz(arg1: int, arg2: str, arg3: List[int]) -> int:
    "Will be included in the generated documentation."

# Any function/method/class not decorated with @dock is ignored
def qux():
    "This function is deliberately ignored to not clutter public API."

class IgnoredClass:
    "Not included in the documentation."

@dock
class IncludedClass:
    "This docstring is included."

    @dock
    def __init__(self):
        "Included"

    @dock()
    def included(self):
        "Included"

    def ignored(self):
        "Ignored"

    @dock(raises='A BoffinException')
    def boffin(self):
        raise BoffinException()
```

*"Deliberate documentation*" refers to the purposeful limitation that only
functions, methods, and classes decorated with the `@dock` decorator will be
included in the generated output.

This moniker is in reference to the common practice of hoping that a given
documentation generator will be able to properly parse out data from docstrings.
A way of thinking about alternatives to deliberate documentation is *"haphazard
documentation"*, or, *"documentation that has a chance of failure"*.

Other issues with existing documentation generators is that they rely too
heavily on placing all relevant documentation details in docstrings. These
details can include:

* Function argument types
* Function return types
* Class fields (including static fields)
* Expected arguments to functions that take variable arguments.

Dock takes all of these requirements and defines them formally. The `@dock`
decorator takes a set of known arguments that can be used to specify extra
documentation for things that Python makes difficult such as any exceptions that
can be raised from a function.

## Features

* Simple, 1-file HTML output
* Small and fast: Dock decorator and CLI are about 500 lines of code combined
* Pure Python
* Crossplatform: Works on Any Platform Python runs (Windows, MacOS, Linux, etc.)
* Multi-line strings are properly dedented
* Markdown syntax supported in **Dock**strings

## Documentation

> Ironically, Dock purposely *does not have hosted docs*. Everything you need to
know is in this README.

### @dock Decorator

There are several built-in documentation sections that can be used:
* returns: Explaination of return value.
* raises: Explaination of return value.
* short: One liner briefly describing what the callable does.

All other keyword arguments are handled differently depending on the type of
the callable (function/method or class):
* Function: kwargs matching annotated arguments describe those arguments.
Leftover kwargs are added to output as entirely new sections.
* Class: Only kwargs are used and are used to desribe class fields.

### Command Line Interface

> NOTE: It is important that you change directory to the root of a given project
so that Dock will be able to properly handle relative imports to their fullest.

```bash
$ cd to-project-root/  # Important
$ dock module.py
$ dock package
$ dock module.py --show  # Generate temp docs and open in system web browser
$ dock package --show
```

## Notes

* Dock doesn't work well with nested functions because function bodies are not
evaluated until they are called. What this means is that if you want to docment
a nested function, Dock won't be able to generate docs for it since it can only
see the objects that are within the module's global scope or can be introspected
off of a given class.

* The `@dock` decorator should be placed before any other decorators on top of the
function although this may be customized depending how the other decorators
transform the function. Dock's decorator just needs to add a `__dock__`
attribute to the function/class.

* Functions that have arguments that don't have type hints won't show up in the
generated output. It is assumed that if Dock is being used with a function, that
function needs to have proper type hints.
