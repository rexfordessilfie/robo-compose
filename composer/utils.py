from typing import List, Any
import random


def next_wrap(current: Any, elements: List[Any], overlap_size: int = 0):
    """
    Get the next element in a wrap-able overlap-able list.

    Example:
        Given elements=[b, N, #], and overlap_size=1, we have that the next accidental after b, or # is N.
        i.e. a flat or sharp become natural when we raise it.
    """
    current_idx = elements.index(current)
    inside_overlap = current_idx > len(elements) - 1 - overlap_size
    idx = current_idx + 1 + (overlap_size if inside_overlap else 0)
    idx = idx % len(elements)
    return elements[idx]


def prev_wrap(current: Any, elements: List[Any], overlap_size: int = 0):
    """
    Get the previous element in a wrap-able overlap-able list.

    Example:
        Given elements=[b, N, #], and overlap_size=1, we have that the next accidental after b, or # is N.
        i.e. a flat or sharp become natural when we lower it.
    """
    current_idx = elements.index(current)
    inside_overlap = current_idx < overlap_size
    idx = current_idx - 1 - (overlap_size if inside_overlap else 0)
    idx = idx % len(elements)
    return elements[idx]


def random_element(elements: List[Any]):
    """
    TODO: add weighted profile to be able to skew the result
    """
    return elements[random.randint(0, len(elements) - 1)]


if __name__ == '__main__':
    pass
