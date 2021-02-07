import sys
from typing import TypeVar, Optional


T = TypeVar('T')


class DockException(Exception):
    """
    Signals that a usage of the `dock` decorator is invalid.
    """


def dock(
    *func_or_class,
    returns: Optional[str] = None,
    raises: Optional[str] = None,
    short: Optional[str] = None,
    **arg_or_field_docs
) -> T:
    """
    Enriches callables with a __dock__ attribute for documentation generation.

    Can be called in the following ways:

    >>> @dock
    >>> @dock()
    >>> @dock(raises='A TypeError if something went wrong')
    >>> @dock(raises='...', Section1='...', Section2='...')

    Can be used as an decorator above classes, methods, and functions.

    There are several built-in documentation sections that can be used:
     - returns: Explaination of return value.
     - raises: Explaination of return value.
     - short: One liner briefly describing what the callable does.

    All other keyword arguments are handled differently depending on the type
    of the callable (function/method or class):
     - Function: kwargs matching annotated arguments describe those arguments.
     - Function: Leftover kwargs are added to output as entirely new sections.
     - Class: Only kwargs are used and are used to desribe class fields.

    Any valid Markdown string is supported but may interfere with existing
    generation. To be the most precise, Dock documentation strings
    (dockstrings) can match Markdeep format, but advanced features of Markdeep
    are not guaranteed to work well with existing output.

    Documentation for Markdeep: https://casual-effects.com/markdeep/
    """

    def inner(func_or_class: T) -> T:
        """
        Closure that has access to `returns`, `raises`, and
        `arg_or_field_docs` due to the enclosing `if` statement.
        """
        if isinstance(func_or_class, type):
            func_or_class.__dock__ = {'fields': arg_or_field_docs}

        else:
            argument_names = set(
                getattr(func_or_class, '__annotations__', {}).keys()
            )

            argument_descriptions = {}
            sections = {}

            for key, value in arg_or_field_docs.items():
                if key in argument_names:
                    argument_descriptions[key] = value
                else:
                    sections[key] = value

            func_or_class.__dock__ = {
                'returns': returns,
                'raises': raises,
                'arguments': argument_descriptions,
                'short': short,
                'sections': sections
            }

        return func_or_class

    # Takes exactly 0 or 1 positional arguments
    if len(func_or_class) not in {0, 1}:
        raise DockException(
            f'Invalid usage of the `dock` decorator for {func_or_class}. '
            f'Please use as a decorator atop classes, methods, and functions.'
        )

    # Handle: @dock
    elif func_or_class:
        (func_or_class,) = func_or_class

        if isinstance(func_or_class, type):
            func_or_class.__dock__ = {'fields': {}}
        else:
            func_or_class.__dock__ = {
                'returns': None,
                'raises': None,
                'short': None,
                'arguments': {},
                'sections': {}
            }

        return func_or_class

    else:
        return inner


# TODO(pebaz): Flesh this out if it seems useful
# def dock_help(obj: T) -> None:
#     if hasattr(obj, '__dock__'):
#         print(f'Help for {type(obj)}:')
#         print(obj.__dock__)
# dock.help = dock_help


# Allows module to be called directly after being imported
sys.modules[__name__] = dock
