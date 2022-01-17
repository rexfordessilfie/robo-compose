import pytest
import sys

from composer.utils import next_wrap, prev_wrap


def test_next_wrap():
    elements = [1, 2, 3, 4]

    assert next_wrap(1, elements) == 2
    assert next_wrap(2, elements) == 3
    assert next_wrap(3, elements) == 4
    assert next_wrap(4, elements) == 1

    elements2 = [1]
    assert next_wrap(1, elements2) == 1


def test_next_wrap_with_overlap():
    elements = [1, 2, 3, 4]

    assert next_wrap(1, elements, overlap_size=1) == 2
    assert next_wrap(2, elements, overlap_size=1) == 3
    assert next_wrap(3, elements, overlap_size=1) == 4
    assert next_wrap(4, elements, overlap_size=1) == 2

    assert next_wrap(1, elements, overlap_size=2) == 2
    assert next_wrap(2, elements, overlap_size=2) == 3
    assert next_wrap(3, elements, overlap_size=2) == 2
    assert next_wrap(4, elements, overlap_size=2) == 3

    assert next_wrap(1, elements, overlap_size=3) == 2
    assert next_wrap(2, elements, overlap_size=3) == 2
    assert next_wrap(3, elements, overlap_size=3) == 3
    assert next_wrap(4, elements, overlap_size=3) == 4

    assert next_wrap(1, elements, overlap_size=4) == 2
    assert next_wrap(2, elements, overlap_size=4) == 3
    assert next_wrap(3, elements, overlap_size=4) == 4
    assert next_wrap(4, elements, overlap_size=4) == 1

    assert next_wrap(1, elements, overlap_size=5) == 3
    assert next_wrap(2, elements, overlap_size=5) == 4
    assert next_wrap(3, elements, overlap_size=5) == 1
    assert next_wrap(4, elements, overlap_size=5) == 2

    elements2 = [1]
    assert next_wrap(1, elements2) == 1


def test_prev_wrap():
    elements = [1, 2, 3, 4]

    assert prev_wrap(1, elements) == 4
    assert prev_wrap(2, elements) == 1
    assert prev_wrap(3, elements) == 2
    assert prev_wrap(4, elements) == 3

    elements2 = [1]
    assert prev_wrap(1, elements2) == 1


def test_prev_wrap_with_overlap():
    elements = [1, 2, 3, 4]

    assert prev_wrap(1, elements, overlap_size=1) == 3
    assert prev_wrap(2, elements, overlap_size=1) == 1
    assert prev_wrap(3, elements, overlap_size=1) == 2
    assert prev_wrap(4, elements, overlap_size=1) == 3

    assert prev_wrap(1, elements, overlap_size=2) == 2
    assert prev_wrap(2, elements, overlap_size=2) == 3
    assert prev_wrap(3, elements, overlap_size=2) == 2
    assert prev_wrap(4, elements, overlap_size=2) == 3

    assert prev_wrap(1, elements, overlap_size=3) == 1
    assert prev_wrap(2, elements, overlap_size=3) == 2
    assert prev_wrap(3, elements, overlap_size=3) == 3
    assert prev_wrap(4, elements, overlap_size=3) == 3

    assert prev_wrap(1, elements, overlap_size=4) == 4
    assert prev_wrap(2, elements, overlap_size=4) == 1
    assert prev_wrap(3, elements, overlap_size=4) == 2
    assert prev_wrap(4, elements, overlap_size=4) == 3

    assert prev_wrap(1, elements, overlap_size=5) == 3
    assert prev_wrap(2, elements, overlap_size=5) == 4
    assert prev_wrap(3, elements, overlap_size=5) == 1
    assert prev_wrap(4, elements, overlap_size=5) == 2


if __name__ == '__main__':
    pytest.main(sys.argv)
