from intervals import EqualTemperament as et


class IntervalsRelatedToStartFrequency:
    MAJOR = [
        et.UNISON.value, et.MAJOR_SECOND.value, et.MAJOR_THIRD.value,
        et.PERFECT_FOURTH.value, et.PERFECT_FIFTH.value, et.MAJOR_SIXTH.value,
        et.MAJOR_SEVENTH.value, et.OCTAVE.value
    ]

    MINOR = []


class IntervalsRelatedToNextNote:
    CHROMATIC = [
        et.UNISON.value, et.SEMITONE.value, et.SEMITONE.value,
        et.SEMITONE.value, et.SEMITONE.value, et.SEMITONE.value,
        et.SEMITONE.value, et.SEMITONE.value, et.SEMITONE.value,
        et.SEMITONE.value, et.SEMITONE.value, et.SEMITONE.value,
        et.SEMITONE.value
    ]


class ScaleBuilder:
    def __init__(
        self,
        interval_list=[],
        frequency_list=[],
        intervals_relative_to_start=False,
        intervals_relative_to_next=False,
    ):
        self.interval_list = interval_list
        self.intervals_relative_to_start = intervals_relative_to_start
        self.intervals_relative_to_next = intervals_relative_to_next
        self.frequency_list = frequency_list

    def build(self, start_frequency):
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
                    next_interval = current_frequency * interval
                    scale.append(next_interval)
                    current_frequency = next_interval
                return scale


class ScaleFactory:
    '''Exposes functions to get a scale builder or to build a scale and return it. '''
    MajorScaleBuilder = ScaleBuilder(
        interval_list=IntervalsRelatedToStartFrequency.MAJOR,
        intervals_relative_to_start=True)

    MinorScaleBuilder = ScaleBuilder(
        interval_list=IntervalsRelatedToStartFrequency.MINOR,
        intervals_relative_to_start=True)

    ChromaticScaleBuilder = ScaleBuilder(
        interval_list=IntervalsRelatedToNextNote.CHROMATIC,
        intervals_relative_to_next=True)

    def __init__(self):
        pass

    def get_scale_builder(self, mode):
        if (mode == "major"):
            return self.MajorScaleBuilder

        if (mode == "minor"):
            return self.MinorScaleBuilder

        if (mode == "chromatic"):
            return self.ChromaticScaleBuilder

    def get_scale(self, start_frequency, mode):
        scale_builder = self.get_scale_builder(mode)
        scale = scale_builder.build(start_frequency)
        return scale
