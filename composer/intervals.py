from typing import Union


class Interval:
    """TODO: extend built-in float?"""
    def __init__(self, value: float):
        self.value = float(value)
        self.inverse = float(1 / value)

    def __str__(self):
        return f'Interval:{self.value}'

    def __repr__(self):
        return str(self)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Interval):
            return self.value == other.value

        return self.value == other

    # TODO: reconsider what it means to add an interval. Truly increasing an interval by x amount constitutes
    #  multiplying it
    def __add__(self, other: Union[object, float]):
        if isinstance(other, Interval):
            return Interval(self.value + other.value)

        return self.value + other

    def __mul__(self, other: Union[object, float]):
        if isinstance(other, Interval):
            return Interval(self.value * other.value)

        return self.value * other

    # reverse multiplication same as __mul__, so that: a * interval = interval * a
    __rmul__ = __mul__


# Interval Definitions


# TODO: make this inherit from Temperament so we can talk about intervals without knowing the specific one being used

class EqualTemperament:
    base = 2 ** (1 / 12)

    UNISON = Interval(base ** 0)

    MINOR_SECOND = m2 = Interval(base ** 1)
    MAJOR_SECOND = M2 = Interval(base ** 2)

    MINOR_THIRD = m3 = Interval(base ** 3)
    MAJOR_THIRD = M3 = Interval(base ** 4)

    PERFECT_FOURTH = P4 = Interval(base ** 5)

    TRITONE = Interval(base ** 6)
    DIMINISHED_FIFTH = D5 = TRITONE
    AUGMENTED_FOURTH = A4 = TRITONE

    PERFECT_FIFTH = P5 = Interval(base ** 7)

    MINOR_SIXTH = m6 = Interval(base ** 8)
    MAJOR_SIXTH = M6 = Interval(base ** 9)

    MINOR_SEVENTH = m7 = Interval(base ** 10)
    MAJOR_SEVENTH = M7 = Interval(base ** 11)

    OCTAVE = Interval(base ** 12)

    TONE = MAJOR_SECOND
    SEMITONE = MINOR_SECOND

    @classmethod
    def sharpen(cls, interval: Interval = None, frequency: int = None, count: int = 1):
        final_interval = Interval(cls.base ** count)

        if interval:
            return interval * final_interval

        if frequency:
            return frequency * final_interval.value

    @classmethod
    def flatten(cls, interval: Interval = None, frequency: int = None, count: int = 1):
        final_interval = Interval(cls.base ** count)

        if interval:
            return interval * final_interval.inverse

        if frequency:
            return frequency * final_interval.inverse


class JustIntonation:
    UNISON = Interval(1)

    MINOR_SECOND = m2 = Interval(25 / 24)
    MAJOR_SECOND = M2 = Interval(9 / 8)

    MINOR_THIRD = m3 = Interval(6 / 5)
    MAJOR_THIRD = M3 = Interval(5 / 4)

    PERFECT_FOURTH = P4 = Interval(4 / 3)

    TRITONE = Interval(45 / 32)
    DIMINISHED_FIFTH = D5 = TRITONE
    AUGMENTED_FOURTH = A4 = TRITONE

    PERFECT_FIFTH = P5 = Interval(3 / 2)

    MINOR_SIXTH = m6 = Interval(8 / 5)
    MAJOR_SIXTH = M6 = Interval(5 / 3)

    MINOR_SEVENTH = m7 = Interval(9 / 5)
    MAJOR_SEVENTH = M7 = Interval(15 / 8)

    OCTAVE = Interval(2)

    TONE = MAJOR_SECOND
    SEMITONE = MINOR_SECOND

    @classmethod
    def sharpen(cls, interval: Interval = None, frequency: int = None, count: int = 1):
        final_interval = Interval(cls.m2.value ** count)

        if interval:
            return interval * final_interval

        if frequency:
            return frequency * final_interval.value

    @classmethod
    def flatten(cls, interval: Interval = None, frequency: int = None, count: int = 1):
        final_interval = Interval(cls.m2.value ** count)

        if interval:
            return interval * final_interval.inverse

        if frequency:
            return frequency * final_interval.inverse
