import copy
import math
import random
from dataclasses import dataclass
from typing import Union, Generator, Tuple, List

from composer.intervals import EqualTemperament12
from composer.scales import ScaleFactory, ScaleMode
from composer.utils import next_wrap, prev_wrap, random_element


# TODO: add 'temperament' parameter to pass tuning as argument everywhere EqualTemperament is used

class Accidental:
    FLAT = 'flat'
    NATURAL = 'natural'
    SHARP = 'sharp'

    @staticmethod
    def all(start: str = None):
        """
        Return accidentals in order of 'increase', with natural at 0
        TODO: add support for micro-tonal accidentals?
        """
        default = [Accidental.FLAT, Accidental.NATURAL, Accidental.SHARP]
        if start:
            start_idx = default.index(start)
            return default[start_idx:] + default[:start_idx]
        return default

    @staticmethod
    def next(current: str):
        accidentals = Accidental.all()
        return next_wrap(current, accidentals, overlap_size=1)

    @staticmethod
    def prev(current: str):
        accidentals = Accidental.all()
        return prev_wrap(current, accidentals, overlap_size=1)


class PitchClass:
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'

    @staticmethod
    def all(start: str = None):
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

    @staticmethod
    def sharp(start: str = None):
        """
        Return pitch classes that can be sharpened according to Western music system
        """
        default = [PitchClass.A, PitchClass.C, PitchClass.D, PitchClass.F, PitchClass.G]
        if start:
            if start not in default:
                raise ValueError('start pitch class does not have a sharp')
            start_idx = default.index(start)
            return default[start_idx:] + default[:start_idx]
        return default

    @staticmethod
    def flat(start: str = None):
        """
        Return pitch classes that can be flattened according to Western music system
        """
        default = [PitchClass.A, PitchClass.B, PitchClass.D, PitchClass.E, PitchClass.G]
        if start:
            if start not in default:
                raise ValueError('start pitch class does not have a flat')
            start_idx = default.index(start)
            return default[start_idx:] + default[:start_idx]
        return default

    @staticmethod
    def next(current: str):
        """
        Get the next pitch class after current in Western Music system
        TODO: make this an instance function? Allow for PitchClass('C').next()
        """
        pitch_classes = PitchClass.all()
        return next_wrap(current, pitch_classes)

    @staticmethod
    def prev(current: str):
        """
        Get the previous pitch class from current in Western Music system
        """
        pitch_classes = PitchClass.all()
        return prev_wrap(current, pitch_classes)


@dataclass
class PitchInfo:
    frequency: int = None
    pitch_class: str = None
    accidental: str = None
    register: int = None
    enharmonic_pitch_class: str = None
    enharmonic_accidental: str = None

    def next(self):
        """
        Get the next pitch after the current one.
        """
        pitch_info = copy.deepcopy(self)
        pitch_info.frequency = None

        if pitch_info.accidental == Accidental.FLAT:
            pitch_info.swap_enharmonic()

        if pitch_info.pitch_class in PitchClass.sharp():
            pitch_info.accidental = Accidental.next(pitch_info.accidental)

        if pitch_info.accidental == Accidental.NATURAL:
            pitch_info.pitch_class = PitchClass.next(pitch_info.pitch_class)

        # TODO: update register as well

        return pitch_info

    def prev(self):
        """
        Get the pitch info before the current pitch.
        """
        pitch_info = copy.deepcopy(self)
        pitch_info.frequency = None

        if pitch_info.accidental == Accidental.SHARP:
            pitch_info.swap_enharmonic()

        if pitch_info.pitch_class in PitchClass.flat():
            pitch_info.accidental = Accidental.prev(pitch_info.accidental)

        if pitch_info.accidental == Accidental.NATURAL:
            pitch_info.pitch_class = PitchClass.prev(pitch_info.pitch_class)

        return pitch_info

    def fill_enharmonic(self):
        """
        Fills in the enharmonic information if it is not present.
        """
        if not self.enharmonic_pitch_class or not self.enharmonic_accidental:

            if self.accidental == Accidental.SHARP:
                self.enharmonic_pitch_class = PitchClass.next(self.pitch_class)
                self.enharmonic_accidental = Accidental.FLAT

            elif self.accidental == Accidental.FLAT:
                self.enharmonic_pitch_class = PitchClass.prev(self.pitch_class)
                self.enharmonic_accidental = Accidental.SHARP
            else:
                raise AttributeError(f"enharmonic not supported for accidental: {self.accidental}")

    def swap_enharmonic(self):
        """
        Swaps the enharmonic pitch and accidentals to be the main ones.
        """
        self.fill_enharmonic()

        if not self.enharmonic_pitch_class or not self.enharmonic_accidental:
            raise AttributeError('PitchInfo is missing enharmonic pitch class or accidental')

        self.pitch_class, self.enharmonic_pitch_class = self.enharmonic_pitch_class, self.pitch_class
        self.accidental, self.enharmonic_accidental = self.enharmonic_accidental, self.accidental

    def to_pitch(self):
        """
        Transform the pitch info into a (complete) pitch.
        """
        return Pitch(identifier=self.frequency,
                     pitch_class=self.pitch_class,
                     accidental=self.accidental,
                     register=self.register,
                     enharmonic_pitch_class=self.enharmonic_pitch_class,
                     enharmonic_accidental=self.enharmonic_accidental)


# List of chromatic pitches in the western music system.
# NB: at least one of these pitches must be complete.
# TODO: move this to constants file and with only dicts?
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
    """
    Find the interval between two frequencies.
    """
    return b / a


def is_pitch_complete(p: PitchInfo):
    """
    Check if a pitch/pitch info is complete, i.e. has a pitch class, accidental, frequency and register.
    """
    return p.pitch_class and p.accidental and p.frequency and p.register is not None


def complete_pitch_info_generator(pitches_info: List[PitchInfo] = None) -> Generator[Tuple[PitchInfo, int], None, None]:
    """
    Convenience generator to find a complete pitch from the list of chromatic pitches.
    """
    pitches_info = pitches_info if pitches_info else CHROMATIC_PITCHES_INFO
    for idx, pitch_info in enumerate(pitches_info):
        if is_pitch_complete(pitch_info):
            yield pitch_info, idx


def is_enharmonic_match(a: PitchInfo, b: PitchInfo):
    """
    Check if two pitches are enharmonic matches.
    """
    return (a.enharmonic_pitch_class == b.pitch_class and a.enharmonic_accidental == b.accidental) or \
           (a.pitch_class == b.enharmonic_pitch_class and a.accidental == b.enharmonic_accidental)


def is_matching_pitch_info(a: PitchInfo, b: PitchInfo):
    """
    Check if two pitches have matching information (apart from the frequency).
    """
    return (a.pitch_class == b.pitch_class and a.accidental == b.accidental) or is_enharmonic_match(a, b)


def matching_pitch_info_generator(p: PitchInfo,
                                  pitches_info: List[PitchInfo] = None) -> Generator[Tuple[PitchInfo, int], None, None]:
    """
    Convenience generator for finding a matching pitch from a list of pitches.
    """
    pitches_info = pitches_info if pitches_info else CHROMATIC_PITCHES_INFO
    for idx, pitch_info in enumerate(pitches_info):
        if is_matching_pitch_info(p, pitch_info):
            yield pitch_info, idx


def pitch_info_from_pitch_string(pitch_str: str) -> PitchInfo:
    """
    Parse a pitch string representation. E.g. C#4, A#5, Gb8
    """
    parts = tuple((c for c in pitch_str))
    size = len(parts)

    pitch_class = register = accidental = None

    if size == 1:
        (pitch_class,) = parts
    elif size == 2:
        (pitch_class, register) = parts
    elif size >= 3:
        (pitch_class, accidental, register) = parts[:3]

    accidental = Accidental.SHARP if accidental == '#' \
        else Accidental.FLAT if accidental == 'b' \
        else Accidental.NATURAL

    register = int(register)
    pitch_info = PitchInfo(pitch_class=pitch_class, accidental=accidental)

    matching_chromatic_pitch_info, _ = next(
        matching_pitch_info_generator(pitch_info, CHROMATIC_PITCHES_INFO)
    )

    final_pitch_info = copy.deepcopy(matching_chromatic_pitch_info)

    final_pitch_info.register = register
    final_pitch_info.frequency = frequency_from_pitch_info(final_pitch_info)

    if is_enharmonic_match(pitch_info, matching_chromatic_pitch_info):
        final_pitch_info.swap_enharmonic()

    return final_pitch_info


def pitch_info_from_frequency(frequency: float) -> PitchInfo:
    """
    Determines the pitch information from a frequency.
    """
    reference_pitch, reference_pitch_idx = next(complete_pitch_info_generator())

    # how many times and in what direction do we need to reduce/increase octave
    # to normalize to the same octave range
    normalization_scale = math.floor(math.log(reference_pitch.frequency, EqualTemperament12.OCTAVE.value) -
                                     math.log(frequency, EqualTemperament12.OCTAVE.value))

    # normalize the frequency by multiplying with the normalization interval
    # i.e. the number of octaves we need to normalize the frequency
    normalization_interval = EqualTemperament12.OCTAVE.value ** normalization_scale
    normalized_frequency = frequency * normalization_interval

    normalized_interval = interval_between_frequencies(reference_pitch.frequency,
                                                       normalized_frequency)

    # TODO: maybe get more specific about this rounding? What tolerance are we willing to accept when there are extra
    #   decimals?
    num_semitones_from_reference = round(
        math.log(normalized_interval, EqualTemperament12.MINOR_SECOND.value)
    )

    final_pitch_idx = (reference_pitch_idx +
                       num_semitones_from_reference) % len(CHROMATIC_PITCHES_INFO)

    found_pitch = CHROMATIC_PITCHES_INFO[final_pitch_idx]
    final_pitch = copy.deepcopy(found_pitch)

    final_pitch.register = final_pitch.register + (-normalization_scale)
    final_pitch.frequency = frequency

    return final_pitch


def frequency_from_pitch_info(pitch_info: PitchInfo):
    """
    Determine the frequency from the pitch information.
    """
    reference_pitch, reference_pitch_idx = next(complete_pitch_info_generator())
    matching_pitch, matching_pitch_idx = next(
        matching_pitch_info_generator(PitchInfo(pitch_class=pitch_info.pitch_class,
                                                accidental=pitch_info.accidental)))

    num_semitones_from_reference = abs(matching_pitch_idx - reference_pitch_idx)

    octave_difference = pitch_info.register - matching_pitch.register

    base_frequency = reference_pitch.frequency * (EqualTemperament12.MINOR_SECOND.value ** num_semitones_from_reference)

    final_frequency = base_frequency * (EqualTemperament12.OCTAVE.value ** octave_difference)
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

        is_pitch_string_identifier = isinstance(identifier, str)
        is_frequency_identifier = isinstance(identifier, (int, float))

        frequency = identifier if is_frequency_identifier else None
        pitch_string = identifier if is_pitch_string_identifier else None

        super(Pitch, self).__init__(frequency=frequency,
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

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.frequency},{self.pitch_class},{self.accidental},{self.register}>"

    def next(self):
        return super(Pitch, self).next().to_pitch()

    def prev(self):
        return super(Pitch, self).prev().to_pitch()

    def matches(self,
                other: 'Pitch',
                tolerance=EqualTemperament12.MINOR_SECOND.value / 4
                ) -> bool:
        """
        Two pitches are a match if one pitch's frequency can be expressed
        as the original frequency times a power of 2.
        """
        interval = other.frequency / self.frequency
        octaves_interval = abs(math.log(interval, 2))
        extra_interval_decimal = octaves_interval % 1
        return extra_interval_decimal < tolerance

    @staticmethod
    def random(key_signature: 'KeySignature' = None, register: int = None):
        if key_signature and isinstance(key_signature, KeySignature):
            scale = key_signature.scale
            random_index = random.randrange(0, len(scale))
            return scale[random_index].to_pitch()
        else:
            pitch_class = random_element(PitchClass.all())
            register = register if register else random_element(list(range(2, 6)))  # roughly range of 88-key keyboard
            accidental = random_element([Accidental.FLAT, Accidental.NATURAL]) if pitch_class in PitchClass.flat() \
                else random_element([Accidental.SHARP, Accidental.NATURAL]) if pitch_class in PitchClass.sharp() \
                else Accidental.NATURAL
            return Pitch(pitch_class=pitch_class, accidental=accidental, register=register)


class KeySignature:
    def __init__(self, pitch: Pitch, mode: ScaleMode):
        self.pitch = pitch
        self.mode = mode

    @property
    def scale(self):
        return list(map(Pitch, ScaleFactory.get_scale(self.pitch.frequency,
                                                      self.mode)))


# TODO: in general pass CHROMATIC_PITCHES_INFO as arg (maybe 'base_pitches_info') to allow for different
#   base pitches? We might have to change how we match using the number of semitones
#   potentially other possibilities for base pitches are micro-tonal base pitches where subdivisions will
#   now be a quarter of a semitone. This is a problem for the future!

if __name__ == '__main__':
    print(Pitch('Gb8'))
    print(Pitch(pitch_class=PitchClass.B, accidental=Accidental.FLAT, register=4).prev())
