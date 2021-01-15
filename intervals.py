import math

class Interval:
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        return self.value + other.value

    def __str__(self):
        return f'Interval: {self.value}'        

# Interval Definitions

class EqualTemperament:
    base = 2**(1/12)

    UNISON = Interval(base**0)

    MINOR_SECOND = Interval(base**1)
    MAJOR_SECOND = Interval(base**2)

    MINOR_THIRD = Interval(base**3)
    MAJOR_THIRD = Interval(base**4)

    PERFECT_FOURTH = Interval(base**5)

    TRITONE = Interval(base**6)
    DIMINISHED_FIFTH = TRITONE
    AUGMENTED_FOURTH = TRITONE

    PERFECT_FIFTH = Interval(base**7)

    MINOR_SIXTH = Interval(base**8)
    MAJOR_SIXTH = Interval(base**9)

    MINOR_SEVENTH = Interval(base**10)
    MAJOR_SEVENTH = Interval(base**11)

    OCTAVE = Interval(base**12)

    TONE = MAJOR_SECOND
    SEMITONE = MINOR_SECOND

