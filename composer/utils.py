from typing import List, Any


def next_element(current: str, elements: List[Any], overlap_size: int = 0):
    current_idx = elements.index(current)
    inside_overlap = current_idx > len(elements) - 1 - overlap_size
    idx = current_idx + 1 + (overlap_size if inside_overlap else 0)
    idx = idx % len(elements)
    return elements[idx]


def previous_element(current: str, elements: List[Any], overlap_size: int = 0):
    current_idx = elements.index(current)
    inside_overlap = current_idx < overlap_size
    idx = current_idx - 1 - (overlap_size if inside_overlap else 0)
    return elements[idx]
