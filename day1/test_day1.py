import pytest
from day1 import frequency_counter, flatten_list

@pytest.mark.parametrize(
    "input,expected",
    [
        ([], {}),
        ([1], {1: 1}),
        ([1, 2, 2, 3, 1], {1: 2, 2: 2, 3: 1}),
        ("aab", {"a": 2, "b": 1}),
    ],
)
def test_frequency_counter(input, expected):
    assert frequency_counter(input) == expected

def test_flatten_list_basic():
    assert flatten_list([[1, 2], [3]]) == [1, 2, 3]

def test_flatten_list_empty():
    assert flatten_list([]) == []

def test_flatten_list_with_iterables():
    assert flatten_list([("a",), ["b", "c"]]) == ["a", "b", "c"]