from abc import ABC

from .intervals import Temperament, EqualTemperament12
from .scales import ScaleBuilder, Scale
import re


# TODO: ability to recognize and label the harmonic functions of a progression of chords, given a key?

# TODO: use Enums for classes like this across board?
class ChordQuality:
    MAJOR = 'M'
    MINOR = 'm'
    SUS2 = 'sus2'
    SUS4 = 'sus4'
    DIMINISHED = 'dim'
    AUGMENTED = 'aug'


class Chord(Scale, ABC):
    pass


class MajorChord(Chord):
    @property
    def intervals(self):
        return [self.temperament.temperament_12.UNISON,
                self.temperament.temperament_12.MAJOR_THIRD,
                self.temperament.temperament_12.PERFECT_FIFTH]


class MinorChord(Chord):
    @property
    def intervals(self):
        return [self.temperament.temperament_12.UNISON,
                self.temperament.temperament_12.MINOR_THIRD,
                self.temperament.temperament_12.PERFECT_FIFTH]


class Sus2Chord(Chord):
    @property
    def intervals(self):
        return [self.temperament.temperament_12.UNISON,
                self.temperament.temperament_12.MAJOR_SECOND,
                self.temperament.temperament_12.PERFECT_FIFTH]


class Sus4Chord(Chord):
    @property
    def intervals(self):
        return [self.temperament.temperament_12.UNISON,
                self.temperament.temperament_12.PERFECT_FOURTH,
                self.temperament.temperament_12.PERFECT_FIFTH]


class DiminishedChord(Chord):
    @property
    def intervals(self):
        return [self.temperament.temperament_12.UNISON,
                self.temperament.temperament_12.MINOR_THIRD,
                self.temperament.temperament_12.DIMINISHED_FIFTH]


class AugmentedChord(Chord):
    @property
    def intervals(self):
        return [self.temperament.temperament_12.UNISON,
                self.temperament.temperament_12.MAJOR_THIRD,
                self.temperament.temperament_12.MINOR_SIXTH]


class ChordFactory:
    """Exposes functions to get a scale builder or to build a scale and return it."""

    @classmethod
    def get_chord_builder(cls, quality: str, temperament: Temperament = EqualTemperament12):
        if quality.startswith(ChordQuality.MAJOR):
            return ScaleBuilder(interval_list=MajorChord(temperament).intervals,
                                intervals_relative_to_start=True)

        if quality.startswith(ChordQuality.MINOR):
            return ScaleBuilder(interval_list=MinorChord(temperament).intervals,
                                intervals_relative_to_start=True)

        if quality.startswith(ChordQuality.SUS2):
            return ScaleBuilder(interval_list=Sus2Chord(temperament).intervals,
                                intervals_relative_to_start=True)

        if quality.startswith(ChordQuality.SUS4):
            return ScaleBuilder(interval_list=Sus4Chord(temperament).intervals,
                                intervals_relative_to_start=True)

        if quality.startswith(ChordQuality.DIMINISHED):
            return ScaleBuilder(interval_list=DiminishedChord(temperament).intervals,
                                intervals_relative_to_start=True)

        if quality.startswith(ChordQuality.AUGMENTED):
            return ScaleBuilder(interval_list=AugmentedChord(temperament).intervals,
                                intervals_relative_to_start=True)

    @classmethod
    def get_chord(cls, root_frequency: int, quality: str, temperament: Temperament = EqualTemperament12):
        chord_builder = cls.get_chord_builder(quality, temperament)

        base_chord_quality_regex = r'm|M|sus2|sus4|dim|aug'
        chord_extension_str = re.sub(base_chord_quality_regex, '', quality, count=1)

        chord_extension_regex = r"([Mmb#]\d+)"
        chord_extension_qualities = list(
            filter(None, re.split(chord_extension_regex, chord_extension_str)))

        def get_interval_from_extension_quality(q: str):
            try:
                return temperament.aliased_interval(q)
            # TODO: this no longer throws. Do we want it to?
            except AttributeError:
                raise AttributeError(f'unrecognized interval quality: {q}')

        chord_extension_intervals = [get_interval_from_extension_quality(q) for q in chord_extension_qualities]
        chord = chord_builder.build(root_frequency, extended_intervals=chord_extension_intervals)
        chord.sort()
        return chord


if __name__ == '__main__':
    print(ChordFactory.get_chord(440, 'augM7b13#4'))
