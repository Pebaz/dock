import inspect
import importlib.util


def import_(filename: str) -> ['MODULE']:
    spec = importlib.util.spec_from_file_location('source', filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dock(**kwargs):
    def wrapper(func):
        func.__dock__ = kwargs
        return func
    return wrapper


if __name__ == '__main__':
    source = import_('main.py')

    for var in source.__dict__.values():
        if hasattr(var, '__name__') and var.__name__.startswith('__'):
            continue
        
        if callable(var):
            print(var, inspect.getfile(var))
