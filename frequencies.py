import copy
from intervals import EqualTemperament as et
from main import Accidental as al, Pitch, PitchClass as pc
import math


KEYBOARD_PITCHES = [
    # Pitch<A,natural,4>
    Pitch(pitch_class=pc.A,
          accidental=al.NATURAL,
          register=4,
          frequency=440),

    # Pitch<A,sharp,4>
    Pitch(pitch_class=pc.A,
          accidental=al.SHARP,
          enharmonic_pitch_class=pc.B,
          enharmonic_accidental=al.FLAT,
          register=4,),

    # Pitch<B,natural,4>
    Pitch(pitch_class=pc.B,
          accidental=al.NATURAL,
          register=4),

    # Pitch<C,natural,5>
    Pitch(pitch_class=pc.C,
          accidental=al.NATURAL,
          register=5),

    # Pitch<C,sharp,5>
    Pitch(pitch_class=pc.C,
          accidental=al.SHARP,
          enharmonic_pitch_class=pc.D,
          enharmonic_accidental=al.FLAT,
          register=5,),

    # Pitch<D,natural,5>
    Pitch(pitch_class=pc.D,
          accidental=al.NATURAL,
          register=5),

    # Pitch<D,sharp,5>
    Pitch(pitch_class=pc.D,
          accidental=al.SHARP,
          enharmonic_pitch_class=pc.E,
          enharmonic_accidental=al.FLAT,
          register=5,),

    # Pitch<E,natural,5>
    Pitch(pitch_class=pc.E,
          accidental=al.NATURAL,
          register=5),

    # Pitch<F,natural,5>
    Pitch(pitch_class=pc.F,
          accidental=al.NATURAL,
          register=5),

    # Pitch<F,sharp,5>
    Pitch(pitch_class=pc.F,
          accidental=al.SHARP,
          enharmonic_pitch_class=pc.G,
          enharmonic_accidental=al.FLAT,
          register=5,
          ),

    # Pitch<G,natural,5>
    Pitch(pitch_class=pc.G,
          accidental=al.NATURAL,
          register=5),

    # Pitch<G,sharp,5>
    Pitch(pitch_class=pc.G,
          accidental=al.SHARP,
          enharmonic_accidental=pc.A,
          enharmonic_pitch_class=al.FLAT,
          register=5,),
]


def interval_between(a: float, b: float):
    return b / a


def is_above_octave_range(a: float, b: float):
    return interval_between(a, b) >= et.OCTAVE.value


def is_below_octave_range(a: float, b: float):
    return interval_between(a, b) < et.UNISON.value


def pitch_from_frequency(frequency: float):
    reference_pitch = next(filter(lambda p: p.pitch_class == pc.A and p.accidental == al.NATURAL,
                                  KEYBOARD_PITCHES), None)

    normalized_interval = frequency / reference_pitch.frequency
    normalization_scale = 0

    # normalize frequency to same octave
    while True:
        below_octave_range = is_below_octave_range(
            reference_pitch.frequency, reference_pitch.frequency * normalized_interval)

        above_octave_range = is_above_octave_range(
            reference_pitch.frequency, reference_pitch.frequency * normalized_interval)

        if below_octave_range:
            normalized_interval *= float(2)
            normalization_scale -= 1
        elif above_octave_range:
            normalized_interval /= float(2)
            normalization_scale += 1
        else:
            break

    num_semitones_from_reference = round(
        math.log(normalized_interval, et.SEMITONE.value)
    )

    reference_pitch_idx = next(i for i, v in enumerate(
        KEYBOARD_PITCHES) if KEYBOARD_PITCHES[i].pitch_class == reference_pitch.pitch_class)

    final_pitch_idx = (reference_pitch_idx +
                       num_semitones_from_reference) % len(KEYBOARD_PITCHES)

    found_pitch = KEYBOARD_PITCHES[final_pitch_idx]
    final_pitch = copy.deepcopy(found_pitch)

    final_pitch.register = final_pitch.register + normalization_scale
    final_pitch.frequency = frequency

    return final_pitch


if __name__ == '__main__':
    print(pitch_from_frequency(440))
