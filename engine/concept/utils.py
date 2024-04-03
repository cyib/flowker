from typing import Union

def mergeDicts(*args):
    result = {}
    for dictionary in args:
        result = {**result, **dictionary}
    return result