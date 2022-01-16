import copy
import math

import pytest
import sys
from composer.pitches import PitchClass, PitchInfo, Accidental, Pitch, KeySignature, complete_pitch_info_generator, \
    CHROMATIC_PITCHES_INFO, is_pitch_complete, is_matching_pitch_info, matching_pitch_info_generator, \
    is_enharmonic_match, pitch_info_from_pitch_string, pitch_info_from_frequency


def test_pitch_class_size():
    assert len(PitchClass.get_list()) == 7


def test_swap_enharmonic():
    pitch_info = PitchInfo(pitch_class=PitchClass.G,
                           accidental=Accidental.SHARP,
                           enharmonic_pitch_class=PitchClass.A,
                           enharmonic_accidental=Accidental.FLAT)

    updated_pitch_info = copy.deepcopy(pitch_info)
    updated_pitch_info.swap_enharmonic()

    assert pitch_info.pitch_class == updated_pitch_info.enharmonic_pitch_class
    assert pitch_info.accidental == updated_pitch_info.enharmonic_accidental

    assert pitch_info.enharmonic_pitch_class == updated_pitch_info.pitch_class
    assert pitch_info.enharmonic_accidental == updated_pitch_info.accidental


def test_swap_enharmonic_raises_on_invalid_enharmonic_details():
    pitch_info = PitchInfo(pitch_class=PitchClass.C,
                           accidental=Accidental.NATURAL)

    with pytest.raises(AttributeError):
        pitch_info.swap_enharmonic()


def test_pitch_info_to_pitch():
    # other non-frequency pitch information
    pitch_info = PitchInfo(pitch_class=PitchClass.C,
                           accidental=Accidental.NATURAL,
                           register=4)
    pitch = pitch_info.to_pitch()
    assert pitch.frequency is not None
    assert pitch.pitch_class == pitch_info.pitch_class
    assert pitch.register == pitch_info.register
    assert pitch.accidental == pitch_info.accidental

    # only frequency
    pitch_info2 = PitchInfo(frequency=440)
    pitch2 = pitch_info2.to_pitch()
    assert pitch2.frequency == pitch_info2.frequency
    assert pitch2.pitch_class == PitchClass.A
    assert pitch2.register == 4
    assert pitch2.accidental == Accidental.NATURAL


def test_complete_pitch_info():
    pitch_info_complete = PitchInfo(frequency=440, pitch_class=PitchClass.A, accidental=Accidental.NATURAL, register=4)
    assert is_pitch_complete(pitch_info_complete)

    pitch_info_missing_frequency = PitchInfo(pitch_class=PitchClass.A, accidental=Accidental.NATURAL, register=4)
    assert not is_pitch_complete(pitch_info_missing_frequency)

    pitch_info_missing_register = PitchInfo(frequency=440, pitch_class=PitchClass.A, accidental=Accidental.NATURAL)
    assert not is_pitch_complete(pitch_info_missing_register)

    pitch_info_missing_class = PitchInfo(frequency=440, accidental=Accidental.NATURAL, register=4)
    assert not is_pitch_complete(pitch_info_missing_class)

    pitches_info_list = [pitch_info_complete]
    assert next(complete_pitch_info_generator(pitches_info_list)) is not None


def test_matching_pitch_info():
    pitch_info = PitchInfo(pitch_class=PitchClass.A, accidental=Accidental.NATURAL, register=4)

    matching_pitch_info = PitchInfo(pitch_class=PitchClass.A, accidental=Accidental.NATURAL, register=8)
    assert is_matching_pitch_info(pitch_info, matching_pitch_info)

    wrong_match = PitchInfo(pitch_class=PitchClass.A, accidental=Accidental.FLAT, register=4)
    assert not is_matching_pitch_info(pitch_info, wrong_match)

    pitches_info_list = [matching_pitch_info]
    assert next(matching_pitch_info_generator(pitch_info, pitches_info_list)) is not None

    # test enharmonic match
    pitch_info2 = PitchInfo(pitch_class=PitchClass.G,
                            accidental=Accidental.SHARP,
                            enharmonic_pitch_class=PitchClass.A,
                            enharmonic_accidental=Accidental.FLAT)

    enharmonic_match = PitchInfo(pitch_class=PitchClass.A, accidental=Accidental.FLAT)
    assert is_enharmonic_match(pitch_info2, enharmonic_match)
    assert is_matching_pitch_info(pitch_info2, enharmonic_match)


def test_chromatic_pitches_info():
    assert len(CHROMATIC_PITCHES_INFO) == 12

    # at least one complete pitch to serve as reference
    assert next(complete_pitch_info_generator(CHROMATIC_PITCHES_INFO)) is not None

    # matching directly defined pitch for arbitrary pitch info
    pitch_info = PitchInfo(pitch_class=PitchClass.E, accidental=Accidental.NATURAL, register=10)
    assert next(matching_pitch_info_generator(pitch_info, CHROMATIC_PITCHES_INFO)) is not None

    # matching enharmonic pitch
    enharmonic_pitch_info = PitchInfo(enharmonic_pitch_class=PitchClass.A, enharmonic_accidental=Accidental.FLAT)
    assert next(matching_pitch_info_generator(enharmonic_pitch_info, CHROMATIC_PITCHES_INFO)) is not None


def test_pitch_info_from_pitch_string():
    a_flat_5 = pitch_info_from_pitch_string('Ab5')

    assert math.isclose(830, a_flat_5.frequency, abs_tol=1)
    assert a_flat_5.pitch_class == PitchClass.A
    assert a_flat_5.accidental == Accidental.FLAT

    a_sharp_5 = pitch_info_from_pitch_string('A#5')

    assert math.isclose(932, a_sharp_5.frequency, abs_tol=1)
    assert a_sharp_5.pitch_class == PitchClass.A
    assert a_sharp_5.accidental == Accidental.SHARP


def test_pitch_info_from_frequency():
    a_natural = pitch_info_from_frequency(440)

    assert a_natural.frequency == 440
    assert a_natural.pitch_class == PitchClass.A
    assert a_natural.accidental == Accidental.NATURAL


def test_pitch_matches_other():
    pitch_a = Pitch(440)
    pitch_b = Pitch('A4')
    assert  pitch_a.matches(pitch_b)


def test_random_pitch():
    random_pitch = Pitch.random(key=KeySignature(pitch=Pitch(440), mode='major'))
    assert isinstance(random_pitch, Pitch)
    assert is_pitch_complete(random_pitch)


if __name__ == '__main__':
    pytest.main(sys.argv)
