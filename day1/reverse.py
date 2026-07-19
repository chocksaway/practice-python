def reverse_input(my_input: str) -> str:
    reverse = []
    for ch in my_input:
        reverse.append(ch)

    return ''.join(reversed(reverse))