from intervals import EqualTemperament as et, Interval
from scales import ScaleBuilder
import re

# TODO: make this generic in terms of the temparament it uses?


class ChordIntervalsRelatedToStartFrequency:
    # Major chord
    MAJOR = [et.UNISON,
             et.MAJOR_THIRD,
             et.PERFECT_FIFTH]

    # Minor chords
    MINOR = [et.UNISON,
             et.MINOR_THIRD,
             et.PERFECT_FIFTH]

    # Sus2 chord
    SUS_2 = [et.UNISON,
             et.MAJOR_SECOND,
             et.PERFECT_FIFTH]

    # Sus4 chord
    SUS_4 = [et.UNISON,
             et.PERFECT_FOURTH,
             et.PERFECT_FIFTH]

    # Diminished chord
    DIMINISHED = [et.UNISON,
                  et.MINOR_THIRD,
                  et.DIMINISHED_FIFTH]

    # Diminished chord
    AUGMENTED = [et.UNISON,
                 et.MAJOR_THIRD,
                 et.sharpen(et.PERFECT_FIFTH)]


class ChordFactory:
    '''Exposes functions to get a scale builder or to build a scale and return it. '''
    MajorChordBuilder = ScaleBuilder(
        interval_list=ChordIntervalsRelatedToStartFrequency.MAJOR,
        intervals_relative_to_start=True)

    MinorChordBuilder = ScaleBuilder(
        interval_list=ChordIntervalsRelatedToStartFrequency.MINOR,
        intervals_relative_to_start=True)

    Sus2ChordBuilder = ScaleBuilder(
        interval_list=ChordIntervalsRelatedToStartFrequency.SUS_2,
        intervals_relative_to_start=True)

    Sus4ChordBuilder = ScaleBuilder(
        interval_list=ChordIntervalsRelatedToStartFrequency.SUS_4,
        intervals_relative_to_start=True)

    AugmentedChordBuilder = ScaleBuilder(
        interval_list=ChordIntervalsRelatedToStartFrequency.AUGMENTED,
        intervals_relative_to_start=True)

    DiminishedChordBuilder = ScaleBuilder(
        interval_list=ChordIntervalsRelatedToStartFrequency.DIMINISHED,
        intervals_relative_to_start=True)

    def __init__(cls):
        pass

    @classmethod
    def get_chord_builder(cls, quality: str):
        if (quality.startswith('M')):
            return cls.MajorChordBuilder

        if (quality.startswith('m')):
            return cls.MinorChordBuilder

        if (quality.startswith("sus2")):
            return cls.Sus2ChordBuilder

        if (quality.startswith("sus4")):
            return cls.Sus4ChordBuilder

        if (quality.startswith("dim")):
            return cls.DiminishedChordBuilder

        if (quality.startswith("aug")):
            return cls.AugmentedChordBuilder

    @classmethod
    def get_chord(cls, root_frequency: int, quality: str):
        chord_builder = cls.get_chord_builder(quality)

        # Determine intervals for chord extensions
        base_chord_quality_regex = r'm|M|sus2|sus4|dim|aug'
        extension_str = re.sub(base_chord_quality_regex, '', quality, count=1)

        extension_regex = r"([Mmb#]\d+)"
        extension_qualities = list(
            filter(None, re.split(extension_regex, extension_str)))

        def get_interval_from_extension_quality(q: str):
            # TODO: add support for aliases to allow writing chords with extensions like b13, #11 etc.
            # _q = q.replace('#4', 'A4').replace('b5', 'D4')
            try:
                return getattr(et, q)
            except AttributeError:
                raise AttributeError('unrecognized interval quality')

        extension_intervals = [
            get_interval_from_extension_quality(extension_quality)
            for extension_quality in extension_qualities]

        # TODO: maybe add the extensions as an argument to the build command?
        chord_builder.extend_interval_list(extension_intervals)
        chord = chord_builder.build(root_frequency)
        chord.sort()
        return chord


if __name__ == '__main__':
    print(ChordFactory.get_chord(440, 'augM7'))
