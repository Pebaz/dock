import sys
import importlib
from types import ModuleType
from typing import TypeVar, Optional, List
from pathlib import Path
from collections import deque
from textwrap import dedent


T = TypeVar('T')


class DockException(Exception):
    """
    Signals that a usage of the `dock` decorator is invalid.
    """
    def __init__(self):
        Exception.__init__(self, (
            'Invalid usage of the `dock` decorator. '
            'Please use as a decorator atop classes, methods, and functions.'
        ))


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


# !!!!!!!!!!!!!
IDEA = """
@dock(
    desc='Short one-liner description.',
    description='Longer multi-paragraph description with sections.'

    desc='sadf',
    description=dict(
        section1='asdf',
        section2='asdf'
    )
    usage='',

    # ! Any ARGDOC not a valid arg name is treated as a section!
    other1='',
    other2='asdf'
)
"""


# !!!!!!!!!!!!!
OUTPUT = """
# Module `module name`

## Function `function name`

> *Short description NO NEWLINES.*

### Arguments

- `arg1` (TypeName): *arg description*
- `arg2` (TypeName): *arg description*

Long description
Long description
Long description

Long description
Long description
Long description

### Usage

```python
```

```python
```

### Section1

asdfasdf
asdfasdf

### Section2

asdfasdf
asdfasdf
"""


def dock(returns: str = None, raises: str = None, **arg_or_field_docs) -> T:
    """
    ! Must be defined last so that it can put the annotation on the last func.
    """

    # Handle: @dock
    if callable(returns) or isinstance(returns, type):
        print('CONDITION 1')

        func_or_class = returns

        if isinstance(func_or_class, type):
            func_or_class.__dock__ = {'fields': arg_or_field_docs}
        else:
            func_or_class.__dock__ = {
                'returns': None,
                'raises': None,
                'arguments': {}
            }

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
                func_or_class.__dock__ = {'fields': arg_or_field_docs}

            else:
                func_or_class.__dock__ = {
                    'returns': returns,
                    'raises': raises,
                    'arguments': arg_or_field_docs
                }

            return func_or_class

        return inner

    # Handle bad input: dock(123)
    else:
        raise DockException()


def introspect(obj: T, queue: deque):
    for attr in obj.__dict__.values():
        if hasattr(attr, '__dock__'):
            print(attr, ':', attr.__dock__)
            queue.append(attr)
        
        if isinstance(attr, type):
            introspect(attr, queue)


def get_modules(path: Path) -> List[str]:
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


def generate(obj: T, prev: Optional[T] = None, file=None):
    out = {'file': file} if file else {}
    name = obj.__name__  # ! Explicitely fail if somehow not named
    full_name = getattr(obj, '__qualname__', '').replace('<locals>.', '')

    if isinstance(obj, ModuleType) and name.endswith('__init__'):  # Package
        print('PACKAGE'.ljust(20), name.ljust(20), '->',full_name)

    elif isinstance(obj, ModuleType):  # Module
        print('MODULE'.ljust(20), name.ljust(20), '->',full_name)
    
    elif isinstance(obj, type):  # Class
        print('CLASS'.ljust(20), name.ljust(20), '->',full_name)

    elif callable(obj):  # Method or Function
        # import ipdb; ipdb.set_trace()

        # prev_name = prev.__name__ if prev else __file__

        prev_name = getattr(
            prev,
            '__qualname__',
            prev.__name__ if prev else __file__
        )

        if full_name.startswith(prev_name):  # Method
            print('METHOD'.ljust(20), name.ljust(20), '->',full_name)

        else:  # Function
            print('FUNCTION'.ljust(20), name.ljust(20), '->',full_name)


    # dock = obj.__dock__
    # doc = dedent(getattr(obj, '__doc__', None) or '')
    # ann = getattr(obj, '__annotations__', {})

    # is_class = isinstance(obj, type)
    # lines = [i.strip() for i in doc.splitlines() if i.strip()]
    # short_desc = lines[0].strip()
    # long_desc = '\n'.join(lines[1:])

    # print(f'## {"Class" if is_class else "Function"} {name}\n', **out)
    # # print(f'{doc}\n', **out)
    # print(f'> {short_desc}\n\n', **out)

    # if is_class:  # Class
    #     pass

    # else:  # Function or method
    #     arguments = dock.get('arguments', {})
    #     returns = dock['returns']
    #     raises = dock['raises']

    #     signature_keys = set(ann.keys())
    #     section_keys = set(arguments.keys()).intersection(signature_keys)

    #     print('>>>', signature_keys, section_keys)

    #     if arguments:
    #         print(f'### Arguments\n', **out)

    #         for arg_name, arg_doc in arguments.items():
    #             if arg_name in section_keys:
    #                 continue
    #             print(f'**{arg_name}**: *{arg_doc}*\n', **out)

    #     print(f'{long_desc}\n', **out)

    #     if returns:
    #         print(f'### Returns\n{dock["returns"]}\n', **out)

    #     if raises:
    #         print(f'### Raises\n{dock["raises"]}\n', **out)


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

            queue.append(mod)  # Preserve output order

            introspect(mod, queue)  # Scrape out all __dock__ed members
        except Exception as e:
            print('WARNING: Failed to import', module, ':', e)

    print('*')

    print()
    print('-' * 80)
    print('* Docking')

    foo = open('foo.md', 'w')
    prev = None
    while queue:
        item = queue.popleft()
        generate(item, prev, foo)
        prev = item
        

    # * cls; python dock.py test_dock.py


# Run the CLI or allow the module to be callable
if __name__ == '__main__':
    cli(sys.argv[1:])
else:
	sys.modules[__name__] = dock  
