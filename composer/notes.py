import copy
import random
from typing import List

from composer.pitches import Pitch, PitchClass


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

    def dot(self):
        return self.value * 1.5

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


class TimeSignature:
    def __init__(self, num_beats: int, note_value: float):
        self.num_beats = num_beats
        self.beat_value = note_value


def viable_durations_generator(note_values: List[float],
                               bpm: float,
                               time_signature: TimeSignature,
                               max_duration: float):

    for note_value in sorted(note_values):
        duration = Duration.duration_from_note_value(note_value, bpm, time_signature)
        if not max_duration:
            yield duration
        elif duration < max_duration:
            yield duration
        else:
            break


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
            self.value = Duration.duration_from_note_value(note_value, bpm, time_signature)

    def __repr__(self) -> str:
        return f"Duration<{self.value}>"

    def set_bpm(self, bpm: float):
        pass

    @staticmethod
    def duration_from_note_value(note_value: float,
                                 bpm: float,
                                 time_signature: TimeSignature):
        beat_duration = 60 / bpm
        num_beats_in_note_value = note_value / time_signature.beat_value
        return num_beats_in_note_value * beat_duration

    @staticmethod
    def random(multiplier: float = 1,
               bpm: int = None,
               time_signature: TimeSignature = None,
               max_duration: float = None):
        """
        TODO: get a random duration and return it. If quantized then return something that aligns to a specific
        division of the beat or bpm. Consider time signature??
        """
        if bpm and time_signature:
            note_values = NoteValue.all()
            durations = list(viable_durations_generator(note_values, bpm, time_signature, max_duration))
            # TODO: weighted random. Weight notes in the middle more compared to whole notes and really fast notes.
            #   esp depending on the BPM.
            duration = durations[random.randint(0, len(durations) - 1)]
        else:
            duration = random.random() * multiplier

        return Duration(duration)


class Note:
    def __init__(self, pitch: Pitch = None, duration: Duration = None):
        self.pitch = pitch
        self.duration = duration

    def __repr__(self) -> str:
        return f"Note<{self.pitch},{self.duration}>"

    @staticmethod
    def random(duration_multiplier: float = 1,
               bpm: int = None,
               time_signature: TimeSignature = None,
               max_duration: float = None,
               key_signature=None):

        pitch = Pitch.random(key_signature=key_signature)
        duration = Duration.random(multiplier=duration_multiplier,
                                   time_signature=time_signature,
                                   bpm=bpm,
                                   max_duration=max_duration)

        return Note(pitch=pitch, duration=duration)


if __name__ == '__main__':
    print(PitchClass.all(start=PitchClass.E))
    print(Pitch(440).matches(Pitch(440 * 1.2)))
