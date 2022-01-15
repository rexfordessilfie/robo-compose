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
    """
    Determines the Pitch from frequency
    """
    def is_pitch_complete(p: Pitch):
        return p.pitch_class and p.accidental and p.frequency

    def complete_keyboard_pitch(index=False):
        for idx, pitch in enumerate(KEYBOARD_PITCHES):
            if is_pitch_complete(pitch):
                yield (pitch, idx)

    reference_pitch, reference_pitch_idx = next(complete_keyboard_pitch())

    # how many times and in what direction do we need to reduce/increase octave
    # to normalize to the same octave range
    normalization_scale = math.floor(math.log(reference_pitch.frequency, et.OCTAVE.value) -
                                     math.log(frequency, et.OCTAVE.value))

    # normalize the frequency by multiplying with the normalization interval
    # i.e the number of octaves we need to normalize the frequency
    normalization_interval = et.OCTAVE.value**normalization_scale
    normalized_frequency = frequency * normalization_interval

    normalized_interval = interval_between(reference_pitch.frequency,
                                           normalized_frequency)

    num_semitones_from_reference = round(
        math.log(normalized_interval, et.SEMITONE.value)
    )

    final_pitch_idx = (reference_pitch_idx +
                       num_semitones_from_reference) % len(KEYBOARD_PITCHES)

    found_pitch = KEYBOARD_PITCHES[final_pitch_idx]
    final_pitch = copy.deepcopy(found_pitch)

    final_pitch.register = final_pitch.register + (-normalization_scale)
    final_pitch.frequency = frequency

    return final_pitch


if __name__ == '__main__':
    val = 440 * et.OCTAVE
    print(pitch_from_frequency(val))
