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
    foo = dock(**cases['in'])(lambda: ...)
    assert foo.__dock__ == cases['out'] or cases['in']
