# ordered_utils.py

def ordered_set(iterable):
    """
    Returns a list of unique elements from the iterable, preserving order.
    
    Example:
        ordered_set(['a', 'b', 'a', 'c']) -> ['a', 'b', 'c']
    """
    return list(dict.fromkeys(iterable))
