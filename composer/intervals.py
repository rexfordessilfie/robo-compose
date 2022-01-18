from typing import Union, List


class Interval:
    """TODO: extend built-in float?"""

    def __init__(self, value: float):
        self.value = float(value)
        self.inverse = float(1 / value)

    def __repr__(self):
        return f'Interval<{self.value}>'

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
class Temperament:
    def __init__(self, intervals: List[Interval]):
        self.intervals = intervals
        self.UNISON = intervals[0]
        self.MINOR_SECOND = intervals[1]
        self.MAJOR_SECOND = intervals[2]
        self.MINOR_THIRD = intervals[3]
        self.MAJOR_THIRD = intervals[4]
        self.PERFECT_FOURTH = intervals[5]
        self.TRITONE = intervals[6]
        self.PERFECT_FIFTH = intervals[7]
        self.MINOR_SIXTH = intervals[8]
        self.MAJOR_SIXTH = intervals[9]
        self.MINOR_SEVENTH = intervals[10]
        self.MAJOR_SEVENTH = intervals[11]
        self.OCTAVE = Interval(2)

        self.DIMINISHED_FIFTH = self.AUGMENTED_FOURTH = self.TRITONE

        self._aliases = {
            'm2': self.MINOR_SECOND,
            'M2': self.MAJOR_SECOND,
            'm3': self.MINOR_THIRD,
            'M3': self.MAJOR_THIRD,
            'P4': self.PERFECT_FOURTH,
            '#4': self.TRITONE,
            'b5': self.TRITONE,
            'P5': self.PERFECT_FIFTH,
            'b6': self.MINOR_SIXTH,
            'm6': self.MINOR_SIXTH,
            'M6': self.MAJOR_SIXTH,
            'b7': self.MINOR_SEVENTH,
            'm7': self.MINOR_SEVENTH,
            'M7': self.MAJOR_SEVENTH,
            'b9': self.OCTAVE * self.MINOR_SECOND,
            'M9': self.OCTAVE * self.MAJOR_SECOND,
            'M11': self.OCTAVE * self.PERFECT_FOURTH,
            '#11': self.OCTAVE * self.TRITONE,
            'M13': self.OCTAVE * self.MAJOR_SIXTH,
            'b13': self.OCTAVE * self.MINOR_SIXTH,
        }

    def all(self):
        return self.intervals

    def named_interval(self, name: str):
        return self.__dict__.get(name, None) or self._aliases.get(name, None)


EqualTemperament = Temperament([Interval(2 ** (i / 12)) for i in range(0, 12)])

JustIntonation = Temperament([Interval(1), Interval(25 / 24), Interval(9 / 8),
                              Interval(6 / 5), Interval(5 / 4), Interval(4 / 3),
                              Interval(45 / 32), Interval(3 / 2), Interval(8 / 5),
                              Interval(5 / 3), Interval(9 / 5), Interval(15 / 8)])


def sharpen(value: float,
            amount: Interval = EqualTemperament.MINOR_SECOND,
            count: int = 1):
    return value * Interval(amount.value ** count).value


def flatten(value: float,
            amount: Interval = EqualTemperament.MINOR_SECOND,
            count: int = 1):
    return value * Interval(amount.value ** count).inverse

