from typing import List
from composer.intervals import EqualTemperament, Interval


class ScaleIntervalsRelatedToStartFrequency:
    MAJOR = [
        EqualTemperament.UNISON, EqualTemperament.MAJOR_SECOND, EqualTemperament.MAJOR_THIRD,
        EqualTemperament.PERFECT_FOURTH, EqualTemperament.PERFECT_FIFTH, EqualTemperament.MAJOR_SIXTH,
        EqualTemperament.MAJOR_SEVENTH, EqualTemperament.OCTAVE
    ]

    MINOR = []


class ScaleIntervalsRelatedToNextNote:
    CHROMATIC = [
        EqualTemperament.UNISON, EqualTemperament.SEMITONE, EqualTemperament.SEMITONE,
        EqualTemperament.SEMITONE, EqualTemperament.SEMITONE, EqualTemperament.SEMITONE,
        EqualTemperament.SEMITONE, EqualTemperament.SEMITONE, EqualTemperament.SEMITONE,
        EqualTemperament.SEMITONE, EqualTemperament.SEMITONE, EqualTemperament.SEMITONE,
        EqualTemperament.SEMITONE
    ]


class ScaleBuilder:
    def __init__(
        self,
        interval_list: List[Interval] = None,
        frequency_list: List[int] = None,
        intervals_relative_to_start=False,
        intervals_relative_to_next=False,
    ):
        self.interval_list = interval_list if interval_list else []
        self.intervals_relative_to_start = intervals_relative_to_start if intervals_relative_to_start else []
        self.intervals_relative_to_next = intervals_relative_to_next if intervals_relative_to_next else []
        self.frequency_list = frequency_list if frequency_list else []

    def extend_interval_list(self, intervals: List[Interval]):
        self.interval_list.extend(intervals)

    def build(self, start_frequency: int) -> List[float]:
        use_frequencies = len(self.frequency_list)
        use_intervals = len(self.interval_list)

        if use_frequencies:
            return self.frequency_list
        elif use_intervals:
            if self.intervals_relative_to_start:
                scale = [
                    interval * start_frequency
                    for interval in self.interval_list
                ]
                return scale
            elif self.intervals_relative_to_next:
                scale = []
                current_frequency = start_frequency
                for interval in self.interval_list:
                    next_frequency = current_frequency * interval
                    scale.append(next_frequency)
                    current_frequency = next_frequency
                return scale


class ScaleFactory:
    """Exposes functions to get a scale builder or to build a scale and return it."""
    MajorScaleBuilder = ScaleBuilder(
        interval_list=ScaleIntervalsRelatedToStartFrequency.MAJOR,
        intervals_relative_to_start=True)

    MinorScaleBuilder = ScaleBuilder(
        interval_list=ScaleIntervalsRelatedToStartFrequency.MINOR,
        intervals_relative_to_start=True)

    ChromaticScaleBuilder = ScaleBuilder(
        interval_list=ScaleIntervalsRelatedToNextNote.CHROMATIC,
        intervals_relative_to_next=True)

    def __init__(self):
        pass

    @classmethod
    def get_scale_builder(cls, mode) -> ScaleBuilder:
        if mode == "major":
            return cls.MajorScaleBuilder

        if mode == "minor":
            return cls.MinorScaleBuilder

        if mode == "chromatic":
            return cls.ChromaticScaleBuilder

    @classmethod
    def get_scale(cls, start_frequency, mode) -> List[float]:
        scale_builder = cls.get_scale_builder(mode)
        scale = scale_builder.build(start_frequency)
        return scale


if __name__ == '__main__':
    print(ScaleFactory.get_scale(440, 'chromatic'))
