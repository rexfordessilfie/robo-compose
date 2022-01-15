import math
import random
from composer.pitches import Pitch, PitchClass


class Duration:
    def __init__(self,
                 seconds=0,
                 note_value=None):
        self.duration = seconds
        self.note_value = note_value

    @staticmethod
    def random(max_duration=math.inf,
               quantized=False,
               bpm=None):
        """
        TODO: get a random duration and return it. If quantized then return something that aligns to a specific
        division of the beat or bpm. Consider time signature??
        """
        return random.random() * 1  # fraction of 1 second


class Note:
    def __init__(self, pitch: Pitch = None, duration=None):
        self.pitch = pitch
        self.duration = duration

    def __repr__(self) -> str:
        return f"Note<{self.pitch},{self.duration}>"

    @property
    def frequency(self):
        return self.pitch.frequency

    @staticmethod
    def random(max_duration=math.inf,
               quantized=False,
               bpm=None,
               key=None
               ):

        pitch = Pitch.random(key)
        duration = Duration.random(max_duration=max_duration,
                                   quantized=quantized,
                                   bpm=bpm)
        return Note(pitch=pitch, duration=duration)


if __name__ == '__main__':
    print(PitchClass.get_list(start=PitchClass.E))
    print(Pitch(440).matches(Pitch(440 * 1.2)))
