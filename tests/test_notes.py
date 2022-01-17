import pytest
import sys

from composer.notes import Duration, NoteValue, Note, TimeSignature, duration_from_note_value, note_value_from_duration
from composer.pitches import KeySignature, Pitch


def test_duration_from_note_value():
    duration = duration_from_note_value(note_value=NoteValue.WHOLE, bpm=60, beat_value=NoteValue.WHOLE)
    assert duration == 1

    duration2 = duration_from_note_value(note_value=NoteValue.WHOLE, bpm=60, beat_value=NoteValue.HALF)
    assert duration2 == 2

    duration3 = duration_from_note_value(note_value=NoteValue.WHOLE, bpm=120, beat_value=NoteValue.WHOLE)
    assert duration3 == 0.5


def test_note_value_from_duration():
    note_value = note_value_from_duration(duration=1, bpm=60, beat_value=NoteValue.WHOLE)
    assert note_value == NoteValue.WHOLE

    note_value2 = note_value_from_duration(duration=0.5, bpm=60, beat_value=NoteValue.WHOLE)
    assert note_value2 == NoteValue.HALF


def test_random_duration():
    random_duration1 = Duration.random()
    assert isinstance(random_duration1, Duration)

    multiplier = 1
    random_duration2 = Duration.random(factor=multiplier)
    assert isinstance(random_duration2, Duration)
    assert random_duration2.value < multiplier

    random_duration3 = Duration.random(bpm=60, time_signature=TimeSignature(1, NoteValue.HALF))
    assert isinstance(random_duration3, Duration)


def test_random_duration_with_max_duration():
    max_duration = 0.02
    random_duration = Duration.random(bpm=60, time_signature=TimeSignature(1, NoteValue.HALF),
                                      max_duration=max_duration)
    print(random_duration.value)
    assert isinstance(random_duration, Duration)
    assert random_duration.value < max_duration


def test_random_note():
    note = Note.random(duration_factor=1,
                       bpm=60,
                       time_signature=TimeSignature(4, NoteValue.QUARTER),
                       key_signature=KeySignature(pitch=Pitch(440), mode='major'))

    assert isinstance(note, Note)
    assert isinstance(note.pitch, Pitch)
    assert isinstance(note.duration, Duration)


if __name__ == '__main__':
    pytest.main(sys.argv)
