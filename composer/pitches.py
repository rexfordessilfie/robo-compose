import copy
import math
import random
from dataclasses import dataclass
from typing import Union

from composer.intervals import EqualTemperament, Interval
from composer.scales import ScaleFactory


class Accidental:
    SHARP = 'sharp'
    NATURAL = 'natural'
    FLAT = 'flat'


class PitchClass:
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'

    @staticmethod
    def get_list(start: str = None):
        default = [PitchClass.A,
                   PitchClass.B,
                   PitchClass.C,
                   PitchClass.D,
                   PitchClass.E,
                   PitchClass.F,
                   PitchClass.G]
        if start:
            start_idx = default.index(start)
            return default[start_idx:] + default[:start_idx]
        return default


@dataclass
class PitchInfo:
    # TODO: default register and accidental here to allow for PitchInfo(pitch_class=PitchClass.C).to_pitch() to work?
    frequency: int = None
    pitch_class: str = None
    accidental: str = None
    register: int = None
    enharmonic_pitch_class: str = None
    enharmonic_accidental: str = None

    def swap_enharmonic(self):
        self.pitch_class, self.enharmonic_pitch_class = self.enharmonic_pitch_class, self.pitch_class
        self.accidental, self.enharmonic_accidental = self.enharmonic_accidental, self.accidental

    def to_pitch(self):
        return Pitch(identifier=self.frequency,
                     pitch_class=self.pitch_class,
                     accidental=self.accidental,
                     register=self.register,
                     enharmonic_pitch_class=self.enharmonic_pitch_class,
                     enharmonic_accidental=self.enharmonic_accidental)


"""
List of chromatic pitches in the western music system.
NB: at least one of these pitches must be complete.
"""
CHROMATIC_PITCHES_INFO = [
    # Pitch<A,natural,4>
    PitchInfo(pitch_class=PitchClass.A,
              accidental=Accidental.NATURAL,
              register=4,
              frequency=440),

    # Pitch<A,sharp,4>
    PitchInfo(pitch_class=PitchClass.A,
              accidental=Accidental.SHARP,
              enharmonic_pitch_class=PitchClass.B,
              enharmonic_accidental=Accidental.FLAT,
              register=4),

    # Pitch<B,natural,4>
    PitchInfo(pitch_class=PitchClass.B,
              accidental=Accidental.NATURAL,
              register=4),

    # Pitch<C,natural,5>
    PitchInfo(pitch_class=PitchClass.C,
              accidental=Accidental.NATURAL,
              register=5),

    # Pitch<C,sharp,5>
    PitchInfo(pitch_class=PitchClass.C,
              accidental=Accidental.SHARP,
              enharmonic_pitch_class=PitchClass.D,
              enharmonic_accidental=Accidental.FLAT,
              register=5),

    # Pitch<D,natural,5>
    PitchInfo(pitch_class=PitchClass.D,
              accidental=Accidental.NATURAL,
              register=5),

    # Pitch<D,sharp,5>
    PitchInfo(pitch_class=PitchClass.D,
              accidental=Accidental.SHARP,
              enharmonic_pitch_class=PitchClass.E,
              enharmonic_accidental=Accidental.FLAT,
              register=5),

    # Pitch<E,natural,5>
    PitchInfo(pitch_class=PitchClass.E,
              accidental=Accidental.NATURAL,
              register=5),

    # Pitch<F,natural,5>
    PitchInfo(pitch_class=PitchClass.F,
              accidental=Accidental.NATURAL,
              register=5),

    # Pitch<F,sharp,5>
    PitchInfo(pitch_class=PitchClass.F,
              accidental=Accidental.SHARP,
              enharmonic_pitch_class=PitchClass.G,
              enharmonic_accidental=Accidental.FLAT,
              register=5),

    # Pitch<G,natural,5>
    PitchInfo(pitch_class=PitchClass.G,
              accidental=Accidental.NATURAL,
              register=5),

    # Pitch<G,sharp,5>
    PitchInfo(pitch_class=PitchClass.G,
              accidental=Accidental.SHARP,
              enharmonic_pitch_class=PitchClass.A,
              enharmonic_accidental=Accidental.FLAT,
              register=5)
]


def interval_between_frequencies(a: float, b: float):
    return b / a


def is_above_octave_range(a: float, b: float):
    return interval_between_frequencies(a, b) >= EqualTemperament.OCTAVE.value


def is_below_octave_range(a: float, b: float):
    return interval_between_frequencies(a, b) < EqualTemperament.UNISON.value


def is_pitch_complete(p: PitchInfo):
    return p.pitch_class and p.accidental and p.frequency and p.register is not None


def complete_pitches_info():
    for idx, pitch_info in enumerate(CHROMATIC_PITCHES_INFO):
        if is_pitch_complete(pitch_info):
            yield pitch_info, idx


def is_enharmonic_match(a: PitchInfo, b: PitchInfo):
    return (a.enharmonic_pitch_class == b.pitch_class and a.enharmonic_accidental == b.accidental) or \
           (a.pitch_class == b.enharmonic_pitch_class and a.accidental ==
            b.enharmonic_accidental)


def is_matching_pitch_info(a: PitchInfo, b: PitchInfo):
    return (a.pitch_class == b.pitch_class and a.accidental == b.accidental) or is_enharmonic_match(a, b)


def matching_pitches_info(p: PitchInfo):
    for idx, pitch_info in enumerate(CHROMATIC_PITCHES_INFO):
        if is_matching_pitch_info(p, pitch_info):
            yield pitch_info, idx


def pitch_info_from_pitch_string(pitch_str: str):
    """
    Parse a pitch string representation.
    e.g. C4#, A5#, G8b
    """
    parts = tuple((c for c in pitch_str))
    size = len(parts)

    pitch_class = register = accidental = None

    if size == 1:
        (pitch_class,) = parts
    elif size == 2:
        (pitch_class, register) = parts
    elif size >= 3:
        (pitch_class, register, accidental) = parts[:3]

    accidental = Accidental.SHARP if accidental == '#' \
        else Accidental.FLAT if accidental == 'b' \
        else Accidental.NATURAL

    register = int(register)
    pitch_info = PitchInfo(pitch_class=pitch_class, accidental=accidental)

    matching_chromatic_pitch_info, _ = next(
        matching_pitches_info(pitch_info)
    )

    final_pitch_info = copy.deepcopy(matching_chromatic_pitch_info)

    final_pitch_info.register = register
    final_pitch_info.frequency = frequency_from_pitch_info(final_pitch_info)

    if is_enharmonic_match(pitch_info, matching_chromatic_pitch_info):
        final_pitch_info.swap_enharmonic()

    return final_pitch_info


def pitch_info_from_frequency(frequency: float):
    """
    Determines the Pitch from frequency
    """
    reference_pitch, reference_pitch_idx = next(complete_pitches_info())

    # how many times and in what direction do we need to reduce/increase octave
    # to normalize to the same octave range
    normalization_scale = math.floor(math.log(reference_pitch.frequency, EqualTemperament.OCTAVE.value) -
                                     math.log(frequency, EqualTemperament.OCTAVE.value))

    # normalize the frequency by multiplying with the normalization interval
    # i.e. the number of octaves we need to normalize the frequency
    normalization_interval = EqualTemperament.OCTAVE.value ** normalization_scale
    normalized_frequency = frequency * normalization_interval

    normalized_interval = interval_between_frequencies(reference_pitch.frequency,
                                                       normalized_frequency)

    num_semitones_from_reference = round(
        math.log(normalized_interval, EqualTemperament.SEMITONE.value)
    )

    final_pitch_idx = (reference_pitch_idx +
                       num_semitones_from_reference) % len(CHROMATIC_PITCHES_INFO)

    found_pitch = CHROMATIC_PITCHES_INFO[final_pitch_idx]
    final_pitch = copy.deepcopy(found_pitch)

    final_pitch.register = final_pitch.register + (-normalization_scale)
    final_pitch.frequency = frequency

    return final_pitch


def frequency_from_pitch_info(pitch_info: PitchInfo):
    reference_pitch, reference_pitch_idx = next(complete_pitches_info())
    matching_pitch, matching_pitch_idx = next(matching_pitches_info(PitchInfo(pitch_class=pitch_info.pitch_class,
                                                                              accidental=pitch_info.accidental)))

    num_semitones_from_reference = abs(matching_pitch_idx - reference_pitch_idx)

    octave_difference = pitch_info.register - matching_pitch.register

    base_frequency = reference_pitch.frequency * (EqualTemperament.SEMITONE.value ** num_semitones_from_reference)

    final_frequency = base_frequency * (EqualTemperament.OCTAVE.value ** octave_difference)
    return final_frequency


class Pitch(PitchInfo):
    def __init__(
            self,
            identifier: Union[str, int, float] = None,
            pitch_class=None,
            accidental=Accidental.NATURAL,
            register=4,
            enharmonic_pitch_class=None,
            enharmonic_accidental=None,
    ):

        is_identifier_pitch_string = isinstance(identifier, str)
        is_identifier_frequency = isinstance(identifier, (int, float))

        frequency = identifier if is_identifier_frequency else None
        pitch_string = identifier if is_identifier_pitch_string else None

        super(Pitch, self).__init__(frequency=identifier if is_identifier_frequency else None,
                                    pitch_class=pitch_class,
                                    accidental=accidental,
                                    register=register,
                                    enharmonic_pitch_class=enharmonic_pitch_class,
                                    enharmonic_accidental=enharmonic_accidental)

        if is_pitch_complete(self):
            return

        if frequency is not None:
            pitch_info = pitch_info_from_frequency(frequency)
            self.frequency = frequency
        elif pitch_string is not None:
            pitch_info = pitch_info_from_pitch_string(pitch_string)
            self.frequency = pitch_info.frequency
        else:
            pitch_info = PitchInfo(pitch_class=self.pitch_class,
                                   accidental=self.accidental,
                                   register=self.register)
            self.frequency = frequency_from_pitch_info(pitch_info)

        self.pitch_class = pitch_info.pitch_class
        self.accidental = pitch_info.accidental
        self.register = pitch_info.register
        self.enharmonic_pitch_class = pitch_info.enharmonic_pitch_class
        self.enharmonic_accidental = pitch_info.enharmonic_accidental

    def __str__(self):
        return f"{self.__class__.__name__}<{self.frequency},{self.pitch_class},{self.register},{self.accidental}>"

    def matches(self,
                other: PitchInfo,
                tolerance=EqualTemperament.SEMITONE.value / 4
                ) -> bool:
        """
        Two pitches are a match if one pitch's frequency can be expressed
        as the original frequency times a power of 2.
        """
        interval = other.frequency / self.frequency
        octaves_interval = abs(math.log(interval, 2))

        extra_interval_decimal = octaves_interval % 1
        return extra_interval_decimal < tolerance

    def pitch_at_interval(self, interval: Interval):
        return Pitch(self.frequency * interval.value)

    @staticmethod
    def random(key=None):
        if key and isinstance(key, KeySignature):
            scale = key.get_scale()
            random_index = random.randrange(0, len(scale))
            return scale[random_index]
        else:
            raise ValueError('invalid key signature')


class KeySignature:
    def __init__(self, pitch: Pitch, mode):
        self.pitch = pitch
        self.mode = mode

    def get_scale(self):
        return list(map(Pitch, ScaleFactory.get_scale(self.pitch.frequency,
                                                      self.mode)))


# TODO: in general pass CHROMATIC_PITCHES_INFO as arg (maybe 'base_pitches_info') to allow for different
#   base pitches? We might have to change how we match using the number of semitones
#   potentially other possibilities for base pitches are micro-tonal base pitches where subdivisions will
#   now be a quarter of a semitone. This is a problem for the future!

if __name__ == '__main__':
    print(Pitch('A5'))
