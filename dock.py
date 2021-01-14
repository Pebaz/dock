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



# TODO(pebaz): Spreadsheet().add(Column1='asdf', Column2=3)
# TODO(pebaz): Spreadsheet().add(Other1='asdf', Column2=3)  # Works with empty
# TODO(pebaz): This ensure that a header line is printed


class Table:
    def __init__(self, margin=1, sep='|', align='center'):
        assert align in {'center', 'ljust', 'rjust'}
        self.margin = margin
        self.sep = sep
        self.align = align
        self.rows = []
        self.col_lens = []
    
    def add(self, *cells):
        row = [str(i) for i in cells]

        if not self.rows:
            self.col_lens = [len(i) for i in row]

        self.rows.append(row)

        for i in range(max(len(self.col_lens), len(row))):
            if i >= len(row):
                break
            new_col_len = len(row[i])

            if i >= len(self.col_lens):
                self.col_lens.append(new_col_len)
            col_len = self.col_lens[i]

            if new_col_len > col_len:
                self.col_lens[i] = new_col_len
    
    def show(self):
        start = f'{self.sep}{" " * self.margin}'
        separator = f'{" " * self.margin}{start}'

        for row in self.rows:
            print(start, end='')
            for i, cell in enumerate(row):
                if i >= len(self.col_lens):
                    break
                col_len = self.col_lens[i]
                line = getattr(str(cell), self.align)(col_len)
                print(line, end=separator)
            print()


def dock(returns: str = None, raises: str = None, **arg_or_field_docs) -> T:
    """
    ! Must be defined last so that it can put the annotation on the last func.
    """

    # Handle: @dock
    if callable(returns) or isinstance(returns, type):
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


def group(obj: T, root, table):
    name = obj.__name__  # ! Explicitly fail if somehow not named
    full_name = getattr(obj, '__qualname__', '').replace('<locals>.', '')

    MODULE = getattr(obj, '__module__', getattr(obj, '__package__', name))

    if not full_name:  # Module or Package
        fully_qualified_name = f'{name.replace(".__init__", "")}'

    else:  # Methods or Functions
        fully_qualified_name = f'{MODULE}.{full_name}'
    
    namespace_parts = fully_qualified_name.split('.')
    first_name = namespace_parts.pop(-1)
    namespace = root

    for each_name in namespace_parts:
        namespace = namespace.get(each_name)

    # print('->', fully_qualified_name, namespace)

    if isinstance(obj, ModuleType) and name.endswith('__init__'):  # Package
        table.add('PACKAGE', fully_qualified_name)
        namespace.new(first_name, obj)

    elif isinstance(obj, ModuleType):  # Module
        table.add('MODULE', fully_qualified_name)
        namespace.new(first_name, obj)
    
    elif isinstance(obj, type):  # Class
        table.add('CLASS', fully_qualified_name)
        namespace.new(first_name, obj)

    elif callable(obj):  # Method or Function
        table.add('FUNCTION', fully_qualified_name)
        namespace.add(first_name, obj)


class Namespace:
    def __init__(self, name, obj):
        self.name = name
        self.namespace = {}
        self.ref = obj

    def __str__(self):
        return f'<{self.name}>'

    def new(self, name, obj):
        self.namespace[name] = Namespace(name, obj)
    
    def add(self, name, obj):
        self.namespace[name] = obj
    
    def get(self, name):
        return self.namespace[name]
    
    def as_dict(self):
        result = {'__dock_self__': str(self.ref)}
        for name, value in self.namespace.items():
            if isinstance(value, Namespace):
                result[name] = value.as_dict()
            else:
                result[name] = str(value)
        return result


def generate(namespace, file=None):
    out = {'file': file} if file else {}


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

    print()
    print('-' * 80)
    print('* Modules')
    modules = get_modules(given_path)

    for m in modules:
        print(m)

    print()
    print('-' * 80)
    print('* Introspecting')

    # TODO(pebaz): Extract into function
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

    root = Namespace('root', None)
    # foo = open('foo.md', 'w')
    table = Table()

    while queue:
        item = queue.popleft()
        group(item, root, table)

    table.show()

    print()
    print('-' * 80)
    print('* Namespacing')
    import json
    print(json.dumps(root.as_dict(), indent=4))

    # * cls; python dock.py test_dock.py


# Run the CLI or allow the module to be callable
if __name__ == '__main__':
    cli(sys.argv[1:])
else:
	sys.modules[__name__] = dock  
