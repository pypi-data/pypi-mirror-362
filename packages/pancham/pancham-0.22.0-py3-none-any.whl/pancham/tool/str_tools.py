import re

def remove_and_split(value: str, split_char: str, remove_pattern: str|None=None) -> list[str|int|float]:
    if remove_pattern is not None and type(value) is str:
        value = re.sub(remove_pattern, "", value)

    if type(value) is int or type(value) is float:
        return [value]

    if type(value) is not str:
        return []

    splits = value.split(split_char)
    return [x.strip() for x in splits if len(x.strip()) > 0]