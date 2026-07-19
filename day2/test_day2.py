import pytest
from day2.day2 import is_palindrome, parse_key_value

@pytest.mark.parametrize("s,expected", [
    ("A man, a plan, a canal: Panama", True),
    ("", True),
    ("race a car", False),
    (".,", True),
    ("Able was I ere I saw Elba", True),
])
def test_is_palindrome(s, expected):
    assert is_palindrome(s) is expected

def test_parse_key_value_basic():
    assert parse_key_value("a=1;b=2") == {"a":"1","b":"2"}

def test_parse_key_value_whitespace_and_invalid():
    assert parse_key_value(" a = 10 ; bad ; x= y ") == {"a":"10","x":"y"}

def test_parse_key_value_empty():
    assert parse_key_value("") == {}
