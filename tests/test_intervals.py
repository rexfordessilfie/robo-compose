import pytest
import sys

from composer.intervals import Interval, Temperament, TwelveToneTemperament, EqualTemperament12, JustIntonation


def test_interval():
    interval = Interval(1 / 2)

    assert interval.value == 1 / 2
    assert interval.inverse == 2

    assert interval * 2 == 1
    assert Interval(1) == Interval(1)


def test_temperament():
    my_temperament = Temperament([Interval(1), Interval(1.5), Interval(2)])
    assert len(my_temperament.intervals) == 3

    with pytest.raises(AttributeError):
        assert my_temperament.temperament_12


def test_twelve_tone_temperament():
    my_twelve_tone_temperament = TwelveToneTemperament([Interval(1) for _ in range(12)])
    assert len(my_twelve_tone_temperament.intervals) == 12
    assert len(my_twelve_tone_temperament.temperament_12.intervals) == 12

    with pytest.raises(ValueError):
        TwelveToneTemperament([Interval(1) for _ in range(15)])

    my_15_tone_temperament_with_12_mapping = Temperament([Interval(1) for _ in range(15)],
                                                         temperament_12_indexes=tuple(range(12)))
    assert len(my_15_tone_temperament_with_12_mapping.intervals) == 15
    assert len(my_15_tone_temperament_with_12_mapping.temperament_12.intervals) == 12

    assert len(EqualTemperament12.intervals) == 12
    assert len(EqualTemperament12.temperament_12.intervals) == 12
    for i in range(12):
        assert EqualTemperament12.intervals[i] == EqualTemperament12.temperament_12.intervals[i]

    assert len(JustIntonation.intervals) == 12
    assert len(JustIntonation.temperament_12.intervals) == 12
    for i in range(12):
        assert JustIntonation.intervals[i] == JustIntonation.temperament_12.intervals[i]


if __name__ == '__main__':
    pytest.main(sys.argv)
