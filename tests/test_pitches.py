import copy
import math
import pytest
import sys

from composer.pitches import PitchClass, PitchInfo, Accidental, Pitch, KeySignature, CHROMATIC_PITCHES_INFO, \
    complete_pitch_info_generator, is_pitch_complete, is_matching_pitch_info, matching_pitch_info_generator, \
    is_enharmonic_match, pitch_info_from_pitch_string, pitch_info_from_frequency

from composer.scales import ScaleMode


def test_pitch_class_size():
    assert len(PitchClass.all()) == 7
    assert len(PitchClass.sharp()) == 5
    assert len(PitchClass.flat()) == 5


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
    pitch_info_complete = PitchInfo(frequency=440, pitch_class=PitchClass.A, accidental=Accidental.NATURAL, register=4,
                                    midi_number=69)
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


def test_contiguous_chromatic_pitches_registers():
    _c_natural_pitch_info = PitchInfo(pitch_class=PitchClass.C, accidental=Accidental.NATURAL)
    c_natural_pitch_info, c_natural_pitch_info_idx = next(matching_pitch_info_generator(_c_natural_pitch_info,
                                                                                        CHROMATIC_PITCHES_INFO))
    # register checks
    for i in range(c_natural_pitch_info_idx, len(CHROMATIC_PITCHES_INFO)):
        current = CHROMATIC_PITCHES_INFO[i]
        expected_register = c_natural_pitch_info.register
        assert current.register == expected_register, f"expected pitch after {PitchClass.C}" \
                                                      f"to have same register: {expected_register}"
    for i in range(0, c_natural_pitch_info_idx):
        current = CHROMATIC_PITCHES_INFO[i]
        expected_register = c_natural_pitch_info.register - 1
        assert current.register == expected_register, f"expected pitch after {PitchClass.C}" \
                                                      f"to have one less register: {expected_register}"


def test_contiguous_chromatic_pitches_info_forward():
    # contiguous checks -> forward pass for sharp
    for i in range(0, len(CHROMATIC_PITCHES_INFO) - 1):
        current = CHROMATIC_PITCHES_INFO[i]
        next_ = CHROMATIC_PITCHES_INFO[i + 1]
        expected = current.next()
        assert is_matching_pitch_info(next_, expected), f"expected pitch {expected} " \
                                                        f"at index {i + 1} but found {next_}"


def test_contiguous_chromatic_pitches_info_backward():
    # contiguous checks -> backward pass for flat
    for i in range(len(CHROMATIC_PITCHES_INFO) - 1, -1, -1):
        current = CHROMATIC_PITCHES_INFO[i]
        prev = CHROMATIC_PITCHES_INFO[i - 1]
        expected = current.prev()
        assert is_matching_pitch_info(prev, expected), f"expected pitch {expected} " \
                                                       f"at index {i - 1} but found {prev}"


def test_pitch_info_from_pitch_string():
    a_flat_5 = pitch_info_from_pitch_string('Ab5')

    assert a_flat_5.pitch_class == PitchClass.A
    assert a_flat_5.accidental == Accidental.FLAT
    assert a_flat_5.register == 5

    a_sharp_5 = pitch_info_from_pitch_string('A#5')

    assert a_sharp_5.pitch_class == PitchClass.A
    assert a_sharp_5.accidental == Accidental.SHARP
    assert a_sharp_5.register == 5


def test_pitch_info_from_frequency():
    a_natural = pitch_info_from_frequency(440)

    assert a_natural.frequency == 440
    assert a_natural.pitch_class == PitchClass.A
    assert a_natural.accidental == Accidental.NATURAL


def test_pitch_matches_other():
    pitch_a = Pitch(440)
    pitch_b = Pitch('A4')
    assert pitch_a.matches(pitch_b)


def test_random_pitch():
    random_pitch = Pitch.random(key_signature=KeySignature(pitch=Pitch(440), mode=ScaleMode.MAJOR))
    assert isinstance(random_pitch, Pitch)
    assert is_pitch_complete(random_pitch)


if __name__ == '__main__':
    pytest.main(sys.argv)
