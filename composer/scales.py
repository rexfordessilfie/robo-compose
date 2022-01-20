from typing import List
from enum import Enum
from intervals import EqualTemperament12, Interval, Temperament


class ScaleMode(Enum):
    MAJOR = 'major'
    MINOR = 'minor'
    CHROMATIC = 'chromatic'


class Scale:
    def __init__(self, temperament: Temperament = EqualTemperament12):
        self.temperament = temperament

    @property
    def intervals(self):
        raise NotImplementedError()


class MajorScale(Scale):
    @property
    def intervals(self):
        return [self.temperament.temperament_12.UNISON, self.temperament.temperament_12.MAJOR_SECOND,
                self.temperament.temperament_12.MAJOR_THIRD, self.temperament.temperament_12.PERFECT_FOURTH,
                self.temperament.temperament_12.PERFECT_FIFTH, self.temperament.temperament_12.MAJOR_SIXTH,
                self.temperament.temperament_12.MAJOR_SEVENTH, self.temperament.temperament_12.OCTAVE]


class MinorScale(Scale):
    @property
    def intervals(self):
        return [self.temperament.temperament_12.UNISON, self.temperament.temperament_12.MAJOR_SECOND,
                self.temperament.temperament_12.MINOR_THIRD, self.temperament.temperament_12.PERFECT_FOURTH,
                self.temperament.temperament_12.PERFECT_FIFTH, self.temperament.temperament_12.MINOR_SIXTH,
                self.temperament.temperament_12.MAJOR_SEVENTH, self.temperament.temperament_12.OCTAVE]


class ChromaticScale(Scale):
    @property
    def intervals(self):
        return self.temperament.intervals


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

    def build(self, start_frequency: int, extended_intervals: List[Interval] = None) -> List[float]:
        extended_intervals = extended_intervals if extended_intervals else []
        interval_list = self.interval_list + extended_intervals

        use_frequencies = len(self.frequency_list)
        use_intervals = len(self.interval_list)

        if use_frequencies:
            return self.frequency_list
        elif use_intervals:
            if self.intervals_relative_to_start:
                return [interval * start_frequency for interval in interval_list]
            elif self.intervals_relative_to_next:
                scale = []
                current_frequency = start_frequency
                for interval in interval_list:
                    next_frequency = current_frequency * interval
                    scale.append(next_frequency)
                    current_frequency = next_frequency
                return scale


class ScaleFactory:
    """Exposes functions to get a scale builder or to build a scale and return it."""

    @classmethod
    def get_scale_builder(cls, mode: ScaleMode, temperament: Temperament = EqualTemperament12) -> ScaleBuilder:
        if mode == ScaleMode.MAJOR:
            return ScaleBuilder(interval_list=MajorScale(temperament).intervals,
                                intervals_relative_to_start=True)

        if mode == ScaleMode.MINOR:
            return ScaleBuilder(interval_list=MinorScale(temperament).intervals,
                                intervals_relative_to_start=True)

        if mode == ScaleMode.CHROMATIC:
            return ScaleBuilder(interval_list=ChromaticScale(temperament).intervals,
                                intervals_relative_to_start=True)

    @classmethod
    def get_scale(cls, start_frequency, mode: ScaleMode, temperament: Temperament = EqualTemperament12) -> List[float]:
        scale_builder = cls.get_scale_builder(mode, temperament)
        scale = scale_builder.build(start_frequency)
        return scale


if __name__ == '__main__':
    print(ScaleFactory.get_scale(440, ScaleMode.CHROMATIC))
