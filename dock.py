import sys
from typing import TypeVar
from pathlib import Path


T = TypeVar('T')


def dock(returns: str = None, raises: str = None, **argdocs) -> T:
    """
    * Must be defined last so that it can put the annotation on the last func.

    NOTE: This essentially does the work of introspecting the function now, so
    that Dock doesn't have to do it when generating documentation.
    """

    # TODO(pebaz): Handle empty input @dock
    # TODO(pebaz): Handle class input @dock(class)
    # TODO(pebaz): Handle bad input @dock(3)

    def inner(func: T) -> T:
        ann = getattr(func, '__annotations__', {})

        # TODO(sam): This is not appropriate for functions and classes.
        # TODO(sam): func.__doc__ = DockFunction(func)
        # TODO(sam): func.__doc__ = DockClass(func_or_class)

        func.__dock__ = {
            '__name__': func.__name__,
            '__returntype__': ann.get('return', None),
            '__returns__': returns,
            '__raises__': raises,
            '__annotations__': ann,
            **argdocs
        }


        return func
    return inner


def cli(args):
    if not args:
        print('Dock - Python documentation generator')
        print('Usage: dock (<module filename> | <package path>)')
        quit()

    given_path = Path(args[0])

    if not given_path.exists():
        print(f"{given_path} doesn't exist")
        quit()

    if given_path.is_dir():
        package = given_path
        print(package)
    else:
        module = given_path
        print(module)


# Run the CLI or allow the module to be callable
if __name__ == '__main__':
    cli(sys.argv[1:])
else:
	sys.modules[__name__] = dock  
