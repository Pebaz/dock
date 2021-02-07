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



# @pytest.mark.parametrize('cases', [
#     case({}, {
#         'arguments': {},
#         'raises': None,
#         'returns': None,
#         'sections': {},
#         'short': None
#     }),
#     case({'c': 3}, {
#         'arguments': {'c': 3},
#         'raises': None,
#         'returns': None,
#         'sections': {},
#         'short': None
#     }),
#     case({'raises': 'What?'}, {
#         'arguments': {},
#         'raises': 'What?',
#         'returns': None,
#         'sections': {},
#         'short': None
#     }),
#     case({'c': 3, 'returns': 'What?'}, {
#         'arguments': {'c': 3},
#         'raises': None,
#         'returns': 'What?',
#         'sections': {},
#         'short': None
#     }),
# ])
# def test_dock_arguments(cases):
#     def some_function(a: int, b: float) -> bool:
#         return a > b

#     dock_obj = dock(**cases['in'])(some_function)
#     assert dock_obj.__dock__ == (cases['out'] or cases['in'])


# @pytest.mark.parametrize('cases', [
#     case({}, dict(fields={})),
#     case({'a': 3}, dict(fields={'a': 1})),
#     case({'a': 1, 'Usage': '...'}, dict(fields={'a': 1, 'Usage': '...'})),
# ])
# def test_dock_classes(cases):
#     class SomeClass:
#         "???"

#     dock_obj = dock(**cases['in'])(SomeClass)
#     print(dock_obj.__dock__, cases['out'])
#     assert dock_obj.__dock__ == (cases['out'] or cases['in'])


# @pytest.mark.parametrize('cases', [
#     case({}, dict(fields={})),
#     case({'a': 1}, dict(fields={'a': 1})),
#     case({'a': 1, 'Usage': '...'}, dict(fields={'a': 1, 'Usage': '...'})),
# ])
# def test_dock_class_methods(cases):
#     class SomeClass:
#         def foo(self):
#             "???"

#     dock_obj = dock(**cases['in'])(SomeClass)
#     assert dock_obj.__dock__ == (cases['out'] or cases['in'])
