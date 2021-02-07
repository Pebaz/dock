import pytest
import dock


EMPTY_DOCK = {
    'returns': None,
    'raises': None,
    'arguments': {},
    'sections': {},
    'short': None
}


def case(input_, output=None):
    return {'in': input_, 'out': output}


@pytest.mark.parametrize('cases', [
    case(dict(returns='?'), {**EMPTY_DOCK, **dict(returns='?')}),
    case(dict(raises='?'), {**EMPTY_DOCK, **dict(raises='?')}),
    case(dict(short='?'), {**EMPTY_DOCK, **dict(short='?')}),
    case(dict(a=1, b=2), {**EMPTY_DOCK, **{'sections': dict(a=1, b=2)}})
])
def test_dock(cases):
    """
    Simulates:

    @dock(a=1, b=2, c=3)
    def foo():
        ...
    """
    dock_obj = dock(**cases['in'])(lambda: ...)
    assert dock_obj.__dock__ == cases['out']



@pytest.mark.parametrize('cases', [
    case({}, EMPTY_DOCK),
    case(dict(a=1), {**EMPTY_DOCK, **{'arguments': dict(a=1)}}),
    case(dict(a=1, b=2), {**EMPTY_DOCK, **{'arguments': dict(a=1, b=2)}})
])
def test_dock_arguments(cases):
    def some_function(a: int, b: float) -> bool:
        return a > b

    dock_obj = dock(**cases['in'])(some_function)
    assert dock_obj.__dock__ == (cases['out'] or cases['in'])


@pytest.mark.parametrize('cases', [
    case({}, dict(fields={})),
    case({'a': 1}, dict(fields={'a': 1})),
    case({'a': 1, 'Usage': '...'}, dict(fields={'a': 1, 'Usage': '...'})),
])
def test_dock_classes(cases):
    class SomeClass:
        "???"

    dock_obj = dock(**cases['in'])(SomeClass)
    assert dock_obj.__dock__ == (cases['out'] or cases['in'])


@pytest.mark.parametrize('cases', [
    case({}, {**EMPTY_DOCK, **dict(arguments={})}),
    case({'x': 1}, {**EMPTY_DOCK, **dict(arguments={'x': 1})}),
    case({'x': 1, 'y': 2}, {**EMPTY_DOCK, **dict(arguments={'x': 1, 'y': 2})}),
    case(
        {'x': 1, 'y': 2, 'z': 3},
        {**EMPTY_DOCK, **dict(arguments={'x': 1, 'y': 2}, sections=dict(z=3))}
    ),
])
def test_dock_class_methods(cases):
    class SomeClass:
        def foo(self, x: int, y: float):
            "???"

    dock_obj = dock(**cases['in'])(SomeClass.foo)
    assert dock_obj.__dock__ == (cases['out'] or cases['in'])
