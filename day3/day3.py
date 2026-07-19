from typing import List

def eval_rpn(tokens: List[str]) -> int:
    """
    Evaluate the value of an arithmetic expression in Reverse Polish Notation.
    Valid operators are +, -, *, /. Each operand may be an integer or another expression.
    Division between two integers should truncate toward zero.
    """
    stack = []
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                # Truncate division towards zero
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[0]

# def process_tokens(tokens: List[str]) -> int:
#     stack = []
#
#     for token in tokens:
#         if token in {"+", "-", "*", "/"}:
#
#
#
#
#     return 0


def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """
    Return list of maximums for each sliding window of size k.
    If k == 0 return [].
    """
    raise NotImplementedError
