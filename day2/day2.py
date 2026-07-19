from typing import Dict


def is_palindrome(s: str) -> bool:
    s = s.lower()
    s = s.replace(" ", "")
    s = s.replace("-", "")
    s = s.replace(",", "")
    s = s.replace(":", "")

    for i, ch in enumerate(s):
        if ch != s[len(s) - 1 - i]:
            return False

    return True


print(is_palindrome("Able was I ere I saw Elba"))







def parse_key_value(s: str, item_sep: str = ';', kv_sep: str = '=') -> Dict[str, str]:
    """
    Parse a simple key=value string into a dict. Empty/invalid pairs are skipped.
    Example: "a=1;b=2" -> {"a":"1", "b":"2"}
    """

    s = s.replace(" ", "")

    values = [p for p in s.split(item_sep) if p]

    result_map: Dict[str, str] = {}


    for each in values:
        if each[1] == kv_sep:
            print(each)
            single_value = each.split(kv_sep)
            result_map[single_value[0]] = single_value[1]

    return result_map


parse_key_value(" a = 10 ; bad ; x= y ")