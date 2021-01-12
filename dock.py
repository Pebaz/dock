import sys
from typing import TypeVar
from pathlib import Path
from collections import deque
import importlib


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


def dock(returns: str = None, raises: str = None, **arg_or_field_docs) -> T:
    """
    * Must be defined last so that it can put the annotation on the last func.

    NOTE: This essentially does the work of introspecting the function now, so
    that Dock doesn't have to do it when generating documentation.
    """

    # Handle: @dock
    if callable(returns) or isinstance(returns, type):
        print('CONDITION 1')

        func_or_class = returns

        if isinstance(func_or_class, type):
            func_or_class.__dock__ = {**arg_or_field_docs}
        else:
            func_or_class.__dock__ = {'returns': None, 'raises': None}

        return func_or_class

    # Handle: @dock(...)
    elif isinstance(returns, str) or returns is None:
        print('CONDITION 2')

        def inner(func_or_class: T) -> T:
            """
            Closure that has access to `returns`, `raises`, and
            `arg_or_field_docs` due to the enclosing `if` statement.
            """
            if isinstance(func_or_class, type):
                func_or_class.__dock__ = {**arg_or_field_docs}

            else:
                func_or_class.__dock__ = {
                    'returns': returns,
                    'raises': raises,
                    **arg_or_field_docs
                }

            return func_or_class

        return inner




    print('__dock__:', type(returns), callable(returns), isinstance(returns, type), returns)

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
        # ! print(func_or_class)
        if isinstance(func_or_class, type):
            func_or_class.__dock__ = {**arg_or_field_docs}
        else:
            func_or_class.__dock__ = {
                # Don't need to annotation with type (class/func) since we have a direct reference
                'returns': returns,
                'raises': raises,
                **arg_or_field_docs
            }
        return func_or_class

    if isinstance(returns, type) or callable(returns):
        return inner(returns)
    return inner


def introspect(obj: object, queue: deque):
    for attr in obj.__dict__.values():
        if hasattr(attr, '__dock__'):
            print(attr, ':', attr.__dock__)
            queue.append(attr)
        
        if isinstance(attr, type):
            introspect(attr, queue)


def get_modules(path):
    modules = []

    if path.is_dir():
        for entry in path.iterdir():
            modules.extend(get_modules(entry))

    elif path.suffix == '.py':
        mod = '.'.join([*path.parts][:-1] + [path.stem])
        # ? Remove __init__.py's
        modules.append(mod)

    # Ensures that packages (__init__.py) are imported prior to their modules
    modules.sort(
        key=lambda x: x.count('.') - 0.1 if '__init__' in x else x.count('.')
    )

    return modules


def cli(args):
    if not args:
        print('Dock - Python documentation generator')
        print('Usage: dock (<module filename> | <package path>)')
        quit()

    given_path = Path(args[0])

    if not given_path.exists():
        print(f"{given_path} doesn't exist")
        quit()

    # ! THIS IS VITALLY IMPORTANT (prevents site-packages preferal)
    sys.path.insert(0, str(Path().resolve()))

    queue = deque()  # deque is threadsafe for append & popleft. Use it

    print('* Modules')
    modules = get_modules(given_path)

    for m in modules:
        print(m)

    print('*\n')

    print('* Introspecting')

    for module in modules:
        try:
            mod = importlib.import_module(module)

            # Allows other modules to import this module
            sys.modules[module] = mod

            introspect(mod, queue)  # Scrape out all __dock__ed members
        except Exception as e:
            print('WARNING: Failed to import', module, ':', e)

    print('*')

    print()
    print('-' * 80)
    print('* Docking')

    while queue:
        item = queue.popleft()
        name = getattr(item, '__name__', '') + ':'
        print(name.rjust(15), item.__dock__)

    # * cls; python dock.py test_dock.py


# Run the CLI or allow the module to be callable
if __name__ == '__main__':
    cli(sys.argv[1:])
else:
	sys.modules[__name__] = dock  
