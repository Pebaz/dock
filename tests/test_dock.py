import pytest
import dock


def case(input_, output=None):
    return {'in': input_, 'out': output}


@pytest.mark.parametrize('cases', [
    case({'returns': None, 'raises': None}),
    case({'returns': None, 'raises': None, 'a': 'a'}),
    case({'returns': None, 'raises': None, 'a': 'a', 'b': 'b'}),
    case({'returns': None, 'raises': None, 'a': 'a', 'b': 'b', 'c': 'c'}),
    case(dict(returns=None, a='a'), dict(returns=None, raises=None, a='a')),
    case(dict(a='a'), dict(returns=None, raises=None, a='a')),
    case(dict(returns=None, a=3), dict(returns=None, raises=None, a=3)),
])
def test_dock(cases):
    dock_obj = dock(**cases['in'])(lambda: ...)
    assert dock_obj.__dock__ == cases['out'] or cases['in']


@pytest.mark.parametrize('cases', [
    case({}, {
        'arguments': {},
        'raises': None,
        'returns': None,
        'sections': {},
        'short': None
    }),
    case({'c': 3}, {
        'arguments': {'c': 3},
        'raises': None,
        'returns': None,
        'sections': {},
        'short': None
    }),
    case({'raises': 'What?'}, {
        'arguments': {},
        'raises': 'What?',
        'returns': None,
        'sections': {},
        'short': None
    }),
    case({'c': 3, 'returns': 'What?'}, {
        'arguments': {'c': 3},
        'raises': None,
        'returns': 'What?',
        'sections': {},
        'short': None
    }),
])
def test_dock_arguments(cases):
    def some_function(a: int, b: float) -> bool:
        return a > b

    dock_obj = dock(**cases['in'])(some_function)
    assert dock_obj.__dock__ == cases['out'] or cases['in']


@pytest.mark.parametrize('cases', [
    case({}, dict(fields={})),
    case({'a': 1}, dict(fields={'a': 1})),
    case({'a': 1, 'Usage': '...'}, dict(fields={'a': 1, 'Usage': '...'})),
])
def test_dock_classes(cases):
    class SomeClass:
        "???"

    dock_obj = dock(**cases['in'])(SomeClass)
    assert dock_obj.__dock__ == cases['out'] or cases['in']
