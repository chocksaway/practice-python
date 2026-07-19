from typing import Any, Dict, Iterable, List

def frequency_counter(items: Iterable[Any]) -> Dict[Any, int]:
    """     Return a dict mapping each item to its frequency.     """
    d = {}
    for item in items:
        if item in d:
            d[item] += 1
        else:
            d[item] = 1

    return d

def flatten_list(nested: Iterable[Iterable[Any]]) -> List[Any]:
    """    Flatten one level of nesting.     """
    my_list = []
    for each in nested:
        if isinstance(each, Iterable):
            for item in each:
                my_list.append(item)
        else:
            my_list.append(each)

    return my_list