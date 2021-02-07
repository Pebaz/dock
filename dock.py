import sys, time, importlib, inspect, webbrowser
from types import ModuleType
from typing import TypeVar, Optional, List, _GenericAlias
from pathlib import Path
from collections import deque
from textwrap import dedent
from tempfile import NamedTemporaryFile


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
    ! Must be defined last so that it can put the annotation on the last func.
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


# TODO(pebaz): help(some_dock_func) needs to work with the extra doc fields
def dock_help(obj: T) -> None:
    pass
dock.help = dock_help



def introspect(obj: T, queue: deque) -> None:
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


def introspect_modules(modules: List[T], queue: deque) -> None:
    for module in modules:
        try:
            mod = importlib.import_module(module)

            # Allows other modules to import this module
            sys.modules[module] = mod

            queue.append(mod)  # Preserve output order

            introspect(mod, queue)  # Scrape out all __dock__ed members
        except Exception as e:
            print('WARNING: Failed to import', module, ':', e)


def get_absolute_name(obj: T) -> str:
    "Used to create interlinks"

    if not hasattr(obj, '__name__') and isinstance(obj, _GenericAlias):
        name = repr(obj)
    else:
        name = obj.__name__

    # name = obj.__name__  # ! Explicitly fail if somehow not named

    full_name = getattr(obj, '__qualname__', '').replace('<locals>.', '')

    MODULE = getattr(obj, '__module__', getattr(obj, '__package__', name))

    if not full_name:  # Module or Package
        absolute_name = f'{name.replace(".__init__", "")}'

    else:  # Methods or Functions
        absolute_name = f'{MODULE.replace(".__init__", "")}.{full_name}'
    
    return absolute_name


def group(obj: T, root) -> None:
    name = obj.__name__
    fully_qualified_name = get_absolute_name(obj)
    namespace_parts = fully_qualified_name.split('.')
    first_name = namespace_parts.pop(-1)

    namespace = root
    for each_name in namespace_parts:
        namespace = namespace.get(each_name)

    if isinstance(obj, ModuleType) and name.endswith('__init__'):  # Package
        type_to_register = Package(first_name, obj, fully_qualified_name)

    elif isinstance(obj, ModuleType):  # Module
        type_to_register = Module(first_name, obj, fully_qualified_name)
    
    elif isinstance(obj, type):  # Class
        type_to_register = Class(first_name, obj, fully_qualified_name)

    # * Not making a distinction here between methods/functions since this can
    # * get extremely mirky when sorting them out. No meaning is lost anyway.
    elif callable(obj):  # Function
        type_to_register = Function(first_name, obj, fully_qualified_name)

    namespace.new(type_to_register)
    root.register_type(fully_qualified_name, type_to_register)


class Namespace:
    def __init__(self, name, obj, absolute_name):  # ? , output):
        self.name = name
        self.absolute_name = absolute_name
        self.namespace = {}
        self.ref = obj
        self.name_db = {}
        # ? self.output = output

    def register_type(self, type_name, type_class):
        self.name_db[type_name] = type_class

    def __str__(self):
        return f'<NAMESPACE {self.name}>'

    def new(self, namespace):
        self.namespace[namespace.name] = namespace
    
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

    def get_funcs(self):
        return [
            *filter(
                lambda item: isinstance(item, Function),
                self.namespace.values()
            )
        ]

    def get_namespaces(self):
        classes = Namespace, Package, Module, Class
        return [
            *filter(
                lambda item: isinstance(item, classes),
                self.namespace.values()
            )
        ]
        
    def generate(self, name_db, out):
        print(self.header(), **out)


class Package(Namespace):
    def __str__(self):
        return f'<PACKAGE {self.name}>'
    
    def header(self):
        return f'# Package `{get_absolute_name(self.ref)}`'

    def generate(self, name_db, out):
        print(self.header(), '\n', **out)

        # Long description
        if self.ref.__doc__:
            print(dedent(self.ref.__doc__), **out)


class Module(Namespace):
    def __str__(self):
        return f'<MODULE {self.name}>'

    def header(self):
        return f'## Module `{get_absolute_name(self.ref)}`'

    def generate(self, name_db, out):
        print(self.header(), '\n', **out)

        # Long description
        if self.ref.__doc__:
            print(dedent(self.ref.__doc__), **out)

        # Output interlinks for each inner object
        for obj in self.namespace.values():
            absolue = obj.absolute_name
            type_name = obj.__class__.__name__
            print(f'- {type_name} [{obj.name}](#{type_name}-{absolue})', **out)


class Class(Namespace):
    def __str__(self):
        return f'<CLASS {self.name}>'

    def header(self):
        return f'### Class `{get_absolute_name(self.ref)}`'
    
    def generate(self, name_db, out):
        print(self.header(), **out)

        if self.ref.__dock__['fields']:
            print('**Fields**\n', **out)

            for field, desc in self.ref.__dock__['fields'].items():
                print(f'- `{field}`: *{desc}*', **out)

        # Long description
        if self.ref.__doc__:
            print(dedent(self.ref.__doc__), **out)

        # TODO(pebaz): Print out class heirarchy using MRO


class Function:
    def __init__(self, name, obj, absolute_name):  # ? , output):
        self.name = name
        self.absolute_name = absolute_name
        self.ref = obj
        # ? self.output = output

    def __str__(self):
        return f'<FUNCTION {self.name}>'

    def header(self):
        return f'#### Function `{get_absolute_name(self.ref)}`'

    def generate(self, name_db, out):
        print(self.header(), '\n', **out)

        # Short description
        if self.ref.__dock__.get('short'):
            print(f'> {self.ref.__dock__["short"]}\n', **out)

        # Argument Types
        ann = getattr(self.ref, '__annotations__', {})
        if ann:
            print('**Arguments**\n', **out)

            output = {
                k: [get_absolute_name(v) if v else '?', '']
                for k, v in ann.items()
            }

            for argument, desc in self.ref.__dock__['arguments'].items():
                output[argument][1] = f'*{desc}*'

            for argument, (type_, desc) in output.items():
                if argument == 'return':
                    continue

                if type_ in name_db:  # Output interlink instead
                    type_name = name_db[type_].__class__.__name__
                    interlink = f'[{type_}](#{type_name}-{type_})'
                    print(f'- `{argument}` -> {interlink}: {desc}', **out)
                else:
                    print(f'- `{argument}` -> `{type_}`: {desc}', **out)


            print('\n', **out)

            # Return Type
            for argument, (type_, desc) in output.items():
                if argument == 'return':
                    print(f'**Return Type:** `{type_}`', **out)

        print('\n', **out)

        # Long description
        if self.ref.__doc__:
            print(dedent(self.ref.__doc__), **out)

        print('\n', **out)

        # Other sections
        for section_name, section in self.ref.__dock__['sections'].items():
            print(f'\n**{section_name}**\n', **out)
            print(dedent(section), **out)

        print('\n', **out)

        # Source code
        print('<details><summary>Source</summary>', **out)
        print('\n```python', **out)
        print(dedent(inspect.getsource(self.ref)), **out)
        print('```\n', **out)
        print('</details>\n', **out)


def generate_namespace(namespace, name_db, file=None):
    out = {'file': file} if file else {}

    for func in namespace.get_funcs():
        func.generate(name_db, out)

    for item in namespace.get_namespaces():
        item.generate(name_db, out)
        generate_namespace(item, name_db, file)


class MarkdeepStyles:
    __header = r'<link rel="stylesheet" href="https://casual-effects.com/markdeep/latest/{}.css?">'
    DEFAULT = ''
    JOURNAL = __header.format('journal')
    APIDOC = __header.format('apidoc')
    SLATE = __header.format('slate')
    NEWSMAG = __header.format('newsmag')
    WEBSITE = __header.format('website')
    LATEX = __header.format('latex')
    DARK = __header.format('dark')
    SLIDES = __header.format('slides')


MARKDEEP_HEADER = MarkdeepStyles.JOURNAL
MARKDEEP_FOOTER = r'<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="markdeep.min.js" charset="utf-8"></script><script src="https://morgan3d.github.io/markdeep/latest/markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>'


def cli(args):
    if not args or args[0] == '--show':
        print('Dock - Python documentation generator')
        print('Usage: dock (<module filename> | <package path>) [--show]')
        quit()

    only_show = '--show' in args
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
    introspect_modules(modules, queue)

    print('*')

    print()
    print('-' * 80)
    print('* Docking')

    root = Namespace('root', None, '')

    while queue:
        item = queue.popleft()
        group(item, root)

    print()
    print('-' * 80)
    print('* Namespacing')
    import json
    print(json.dumps(root.as_dict(), indent=4))

    print()
    print('-' * 80)
    print('* Generating')

    if only_show:
        output_file = NamedTemporaryFile('w', delete=False, suffix='.html')
    else:
        output_file = open(f'{given_path.stem}.md.html', 'w')

    output_file.write(MARKDEEP_HEADER)
    generate_namespace(root, root.name_db, output_file)
    output_file.write(MARKDEEP_FOOTER)
    output_file.close()

    if only_show:
        normalized_path = output_file.name.replace('\\', '/')
        uri = f'file://{normalized_path}'
        webbrowser.get().open(uri)
        time.sleep(2)
        Path(output_file.name).unlink()


# Run the CLI or allow the module to be callable
if __name__ == '__main__':
    cli(sys.argv[1:])
else:
	sys.modules[__name__] = dock  
