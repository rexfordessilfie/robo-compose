import math
import copy
from composer.intervals import EqualTemperament
from composer.main import Accidental, Pitch, PitchClass

"""
List of chromatic pitches in the western music system.
NB: at least one of these pitches must be complete.
"""
CHROMATIC_PITCHES = [
    # Pitch<A,natural,4>
    Pitch(pitch_class=PitchClass.A,
          accidental=Accidental.NATURAL,
          register=4,
          frequency=440),

    # Pitch<A,sharp,4>
    Pitch(pitch_class=PitchClass.A,
          accidental=Accidental.SHARP,
          enharmonic_pitch_class=PitchClass.B,
          enharmonic_accidental=Accidental.FLAT,
          register=4),

    # Pitch<B,natural,4>
    Pitch(pitch_class=PitchClass.B,
          accidental=Accidental.NATURAL,
          register=4),

    # Pitch<C,natural,5>
    Pitch(pitch_class=PitchClass.C,
          accidental=Accidental.NATURAL,
          register=5),

    # Pitch<C,sharp,5>
    Pitch(pitch_class=PitchClass.C,
          accidental=Accidental.SHARP,
          enharmonic_pitch_class=PitchClass.D,
          enharmonic_accidental=Accidental.FLAT,
          register=5),

    # Pitch<D,natural,5>
    Pitch(pitch_class=PitchClass.D,
          accidental=Accidental.NATURAL,
          register=5),

    # Pitch<D,sharp,5>
    Pitch(pitch_class=PitchClass.D,
          accidental=Accidental.SHARP,
          enharmonic_pitch_class=PitchClass.E,
          enharmonic_accidental=Accidental.FLAT,
          register=5),

    # Pitch<E,natural,5>
    Pitch(pitch_class=PitchClass.E,
          accidental=Accidental.NATURAL,
          register=5),

    # Pitch<F,natural,5>
    Pitch(pitch_class=PitchClass.F,
          accidental=Accidental.NATURAL,
          register=5),

    # Pitch<F,sharp,5>
    Pitch(pitch_class=PitchClass.F,
          accidental=Accidental.SHARP,
          enharmonic_pitch_class=PitchClass.G,
          enharmonic_accidental=Accidental.FLAT,
          register=5),

    # Pitch<G,natural,5>
    Pitch(pitch_class=PitchClass.G,
          accidental=Accidental.NATURAL,
          register=5),

    # Pitch<G,sharp,5>
    Pitch(pitch_class=PitchClass.G,
          accidental=Accidental.SHARP,
          enharmonic_accidental=PitchClass.A,
          enharmonic_pitch_class=Accidental.FLAT,
          register=5),
]


def interval_between(a: float, b: float):
    return b / a


def is_above_octave_range(a: float, b: float):
    return interval_between(a, b) >= EqualTemperament.OCTAVE.value


def is_below_octave_range(a: float, b: float):
    return interval_between(a, b) < EqualTemperament.UNISON.value


def is_pitch_complete(p: Pitch):
    return p.pitch_class and p.accidental and p.frequency


def complete_keyboard_pitch():
    for idx, pitch in enumerate(CHROMATIC_PITCHES):
        if is_pitch_complete(pitch):
            yield pitch, idx


def is_matching_pitch(a: Pitch, b: Pitch):
    return a.pitch_class == b.pitch_class and a.accidental == b.accidental


def matching_keyboard_pitch(p: Pitch):
    for idx, pitch in enumerate(CHROMATIC_PITCHES):
        if is_matching_pitch(p, pitch):
            yield pitch, idx


def pitch_from_pitch_string(pitch_str: str):
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

    frequency = frequency_from_pitch_info(pitch_class=pitch_class,
                                          accidental=accidental,
                                          register=register)

    return Pitch(pitch_class=pitch_class,
                 accidental=accidental,
                 register=register,
                 frequency=frequency)


def pitch_from_frequency(frequency: float):
    """
    Determines the Pitch from frequency
    """
    reference_pitch, reference_pitch_idx = next(complete_keyboard_pitch())

    # how many times and in what direction do we need to reduce/increase octave
    # to normalize to the same octave range
    normalization_scale = math.floor(math.log(reference_pitch.frequency, EqualTemperament.OCTAVE.value) -
                                     math.log(frequency, EqualTemperament.OCTAVE.value))

    # normalize the frequency by multiplying with the normalization interval
    # i.e. the number of octaves we need to normalize the frequency
    normalization_interval = EqualTemperament.OCTAVE.value ** normalization_scale
    normalized_frequency = frequency * normalization_interval

    normalized_interval = interval_between(reference_pitch.frequency,
                                           normalized_frequency)

    num_semitones_from_reference = round(
        math.log(normalized_interval, EqualTemperament.SEMITONE.value)
    )

    final_pitch_idx = (reference_pitch_idx +
                       num_semitones_from_reference) % len(CHROMATIC_PITCHES)

    found_pitch = CHROMATIC_PITCHES[final_pitch_idx]
    final_pitch = copy.deepcopy(found_pitch)

    final_pitch.register = final_pitch.register + (-normalization_scale)
    final_pitch.frequency = frequency

    return final_pitch


def frequency_from_pitch_info(pitch_class: PitchClass = None,
                              register: int = 4,
                              accidental: Accidental = Accidental.NATURAL):

    matching_pitch, matching_pitch_idx = next(
        matching_keyboard_pitch(
            Pitch(pitch_class=pitch_class,
                  accidental=accidental))
    )

    reference_pitch, reference_pitch_idx = next(complete_keyboard_pitch())

    num_semitones_from_reference = abs(
        matching_pitch_idx - reference_pitch_idx)

    octave_difference = register - reference_pitch.register

    base_frequency = reference_pitch.frequency * \
        (EqualTemperament.SEMITONE.value ** num_semitones_from_reference)

    final_frequency = base_frequency * (EqualTemperament.OCTAVE.value ** octave_difference)
    return final_frequency


if __name__ == '__main__':
    print(pitch_from_pitch_string('C4'))
    print(pitch_from_frequency(440))
