import pytest
from day3.day3 import eval_rpn, max_sliding_window

@pytest.mark.parametrize("tokens,expected", [
    (["2","1","+","3","*"], 9),
    (["4","13","5","/","+"], 6),
    (["10","6","9","3","+","-11","*","/","*","17","+","5","+"], 22)
])
def test_eval_rpn(tokens, expected):
    assert eval_rpn(tokens) == expected

def test_max_sliding_window_simple():
    assert max_sliding_window([1,3,-1,-3,5,3,6,7], 3) == [3,3,5,5,6,7]

def test_max_sliding_window_k1_and_edge():
    assert max_sliding_window([1, -1], 1) == [1,-1]
    assert max_sliding_window([], 3) == []
    assert max_sliding_window([1,2,3], 0) == []
