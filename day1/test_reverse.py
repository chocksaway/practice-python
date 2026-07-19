import pytest
from reverse import reverse_input

@pytest.mark.parametrize("input,expected",
     [
        ("miles", "selim"),
    ], )

def test_reverse(input, expected):
    assert reverse_input(input) == expected

