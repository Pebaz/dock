import sys
from typing import TypeVar
from pathlib import Path


T = TypeVar('T')


def dock(returns: str = None, raises: str = None, **argdocs) -> T:
    """
    * Must be defined last so that it can put the annotation on the last func.
    """
    def inner(func: T) -> T:
        func.__dock__ = {'returns' : returns, 'raises' : raises, **argdocs}
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
