import copy
import math
import random

from composer.pitches import Pitch, PitchClass, KeySignature
from composer.utils import random_element


class NoteValue:
    WHOLE = 1
    HALF = 1 / 2
    QUARTER = 1 / 4
    EIGHTH = 1 / 8
    SIXTEENTH = 1 / 16
    THIRTY_SECOND = 1 / 32
    SIXTY_FOURTH = 1 / 64

    def __init__(self, value):
        self.value = value

    def __repr__(self) -> str:
        return f"NoteValue<{self.value}>"

    def dot(self, count: int = 1):
        multiplier = sum([2 ** -i for i in range(0, count + 1)])
        return NoteValue(multiplier * self.value)

    @staticmethod
    def all(size: int = None):
        default = [NoteValue.WHOLE,
                   NoteValue.HALF,
                   NoteValue.QUARTER,
                   NoteValue.EIGHTH,
                   NoteValue.THIRTY_SECOND,
                   NoteValue.SIXTY_FOURTH]

        if not size:
            return default

        if size < len(default):
            return default[:size]

        values = copy.deepcopy(default)
        return values.extend([2 ** -i * default[-1]
                              for i in range(len(default), size)])

    @staticmethod
    def more(start: float, size: int = 1):
        return [2 ** -i * start for i in range(1, size + 1)]


class TimeSignature:
    def __init__(self, num_beats: int, note_value: float):
        self.num_beats = num_beats
        self.beat_value = note_value

    def __repr__(self) -> str:
        return f"TimeSignature<{self.num_beats},{self.beat_value}>"


def duration_from_note_value(note_value: float,
                             bpm: float,
                             beat_value: float):
    beat_duration = 60 / bpm
    num_beats_in_note_value = note_value / beat_value
    return num_beats_in_note_value * beat_duration


def note_value_from_duration(duration: float,
                             bpm: float,
                             beat_value: float):
    beat_duration = 60 / bpm
    return beat_duration * beat_value * duration


def viable_durations_generator(bpm: float,
                               time_signature: TimeSignature,
                               max_duration: float = math.inf,
                               max_note_value: float = None):
    max_duration = duration_from_note_value(max_note_value, bpm, time_signature.beat_value) \
        if max_note_value else max_duration

    note_values = NoteValue.all()
    note_values_min_duration = duration_from_note_value(min(note_values), bpm, time_signature.beat_value)

    if max_duration and max_duration < note_values_min_duration:
        note_values = NoteValue.more(max_duration, 5)

    for note_value in sorted(note_values):
        duration = duration_from_note_value(note_value, bpm, time_signature.beat_value)
        if (not max_duration) or duration <= max_duration:
            yield duration


class Duration:
    def __init__(self,
                 seconds: float = None,
                 note_value: float = None,
                 bpm: int = None,
                 time_signature: TimeSignature = None):

        if seconds is not None:
            self.value = seconds
        else:
            self.bpm = bpm
            self.note_value = note_value
            self.value = duration_from_note_value(note_value, bpm, time_signature.beat_value)

    def __repr__(self) -> str:
        return f"Duration<{self.value}>"

    def set_bpm(self, bpm: float):
        pass

    @staticmethod
    def random(factor: float = 1,
               bpm: int = None,
               time_signature: TimeSignature = None,
               max_duration: float = None,
               max_note_value: float = None):
        """
        TODO: get a random duration and return it. If quantized then return something that aligns to a specific
        division of the beat or bpm. Consider time signature??
        """
        if bpm and time_signature:
            durations = list(viable_durations_generator(bpm, time_signature, max_duration, max_note_value))
            # TODO: weighted random. Weight notes in the middle more compared to whole notes and really fast notes.
            #   esp depending on the BPM.
            return Duration(random_element(durations))
        else:
            duration = random.random() * factor

        return Duration(duration)


class Note:
    def __init__(self, pitch: Pitch = None, duration: Duration = None):
        self.pitch = pitch
        self.duration = duration

    def __repr__(self) -> str:
        return f"Note<{self.pitch},{self.duration}>"

    @staticmethod
    def random(key_signature: KeySignature = None,
               time_signature: TimeSignature = None,
               bpm: int = None,
               max_duration: float = None,
               duration_factor: float = 1):
        pitch = Pitch.random(key_signature=key_signature)
        duration = Duration.random(factor=duration_factor,
                                   time_signature=time_signature,
                                   bpm=bpm,
                                   max_duration=max_duration)

        return Note(pitch=pitch, duration=duration)


if __name__ == '__main__':
    print(PitchClass.all(start=PitchClass.E))
    print(Pitch(440).matches(Pitch(440 * 1.2)))

    print(NoteValue(NoteValue.WHOLE).dot(1))
