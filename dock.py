import sys
from typing import TypeVar
from pathlib import Path
from collections import deque


T = TypeVar('T')





# ! Only the classes/functions/methods marked with __dock__ should be included
# ! in documentation. This is not an all-encompasing documentation generator.


class DockFunction:
    def __init__(self, func):
        ann = getattr(func, '__annotations__', {})
        func.__dock__ = {
            '__name__': func.__name__,
            '__returntype__': ann.get('return', None),
            '__returns__': returns,
            '__raises__': raises,
            '__annotations__': ann,
            **argdocs
        }


class DockClass:
    def __init__(self, class_):
        self.heirarchy = class_.mro()
        self.heirarchy.pop(0)  # Don't list self as it's implied
        print('heirarchy :'.rjust(20), self.heirarchy)

        self.annotations = getattr(class_, '__annotations__', {})
        print('annotations :'.rjust(20), self.annotations)

        self.desciption = class_.__doc__
        print('desciption :'.rjust(20), repr(self.desciption))

        self.name = class_.__name__
        print('name :'.rjust(20), self.name)

        self.inherited_members = set()
        for ancestor in self.heirarchy:
            for member in ancestor.__dict__:
                if not member.startswith('__'):
                    self.inherited_members.add(member)
        print('inherited_members :'.rjust(20), self.inherited_members)

        self.members = {i for i in class_.__dict__ if not i.startswith('__')}
        print('members :'.rjust(20), self.members)


def dock(returns: str = None, raises: str = None, **argdocs) -> T:
    """
    * Must be defined last so that it can put the annotation on the last func.

    NOTE: This essentially does the work of introspecting the function now, so
    that Dock doesn't have to do it when generating documentation.
    """

    # TODO(pebaz): Handle empty input @dock
    # TODO(pebaz): Handle class input @dock(class)
    # TODO(pebaz): Handle bad input @dock(3)

    # TODO(pebaz): @dock, @dock(), and @dock(...) should work.

    # def inner(func_or_class: T) -> T:
    #     if isinstance(func_or_class, type):
    #         func_or_class.__dock__ = DockClass(func_or_class)
    #     else:
    #         func_or_class.__dock__ = DockFunction(func_or_class)
    #     return func_or_class
    # return inner

    def inner(func_or_class: T) -> T:
        print(func_or_class)
        if isinstance(func_or_class, type):
            func_or_class.__dock__ = {**argdocs}
        else:
            func_or_class.__dock__ = {
                # Don't need to annotation with type (class/func) since we have a direct reference
                'returns': returns,
                'raises': raises,
                **argdocs
            }
        return func_or_class

    if isinstance(returns, type) or callable(returns):
        return inner(returns)
    return inner


def import_(filename: Path) -> ['MODULE']:
    import importlib.util
    spec = importlib.util.spec_from_file_location(filename.stem, filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def introspect(obj: object, queue: deque):
    for attr in obj.__dict__.values():
        if hasattr(attr, '__dock__'):
            print(attr, ':', attr.__dock__)
            queue.append(attr)
        
        if isinstance(attr, type):
            introspect(attr, queue)


def cli(args):
    if not args:
        print('Dock - Python documentation generator')
        print('Usage: dock (<module filename> | <package path>)')
        quit()

    given_path = Path(args[0])

    if not given_path.exists():
        print(f"{given_path} doesn't exist")
        quit()

    queue = deque()  # deque is threadsafe for append & popleft. Use it

    if given_path.is_dir():
        package = given_path
        print(package)
    else:
        module = import_(given_path)
        print('Docking:', module)

        introspect(module, queue)

    print()
    print('-' * 80)

    while queue:
        item = queue.popleft()
        print(item.__dock__)


# Run the CLI or allow the module to be callable
if __name__ == '__main__':
    cli(sys.argv[1:])
else:
	sys.modules[__name__] = dock  
