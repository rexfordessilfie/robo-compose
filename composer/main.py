import math
import random
from composer.intervals import EqualTemperament, Interval
from composer.scales import ScaleFactory


class Accidental:
    SHARP = 'sharp'
    NATURAL = 'natural'
    FLAT = 'flat'


class PitchClass:
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'

    @classmethod
    def get_list(cls, start: str = None):
        default = [cls.A, cls.B, cls.C, cls.D, cls.E, cls.F, cls.G]

        if start:
            start_idx = default.index(start)
            return default[start_idx:] + default[:start_idx]

        return default


class KeySignature:
    def __init__(self, pitch: 'Pitch', mode):
        self.pitch = pitch
        self.mode = mode

    def get_scale(self):
        return list(map(Pitch,
                        ScaleFactory.get_scale(self.pitch.frequency,
                                               self.mode)))


class Pitch:
    def __init__(
            self,

            frequency=None,

            # pitch info
            pitch_class=None,
            accidental=Accidental.NATURAL,
            register=4,

            # enharmonic info
            enharmonic_pitch_class=None,
            enharmonic_accidental=None,
    ):
        self.frequency = frequency

        self.pitch_class = pitch_class
        self.accidental = accidental
        self.register = register

        self.enharmonic_pitch_class = enharmonic_pitch_class
        self.enharmonic_accidental = enharmonic_accidental

    def __str__(self):
        return f"Pitch<{self.frequency},{self.pitch_class},{self.accidental},{self.register}>"

    def matches(self,
                other: 'Pitch',
                tolerance=EqualTemperament.SEMITONE.value / 4
                ) -> bool:
        """
        Two pitches are a match if one pitch's frequency can be expressed 
        as the original frequency times a power of 2.
        """
        interval = other.frequency / self.frequency
        octaves_interval = abs(math.log(interval, 2))

        extra_interval_decimal = octaves_interval % 1
        return extra_interval_decimal < tolerance

    def pitch_at_interval(self, interval: Interval):
        return Pitch(frequency=self.frequency * interval.value)

    @staticmethod
    def random(key=None):
        if key and isinstance(key, KeySignature):
            scale = key.get_scale()
            random_index = random.randrange(0, len(scale))
            return Pitch(frequency=scale[random_index])
        else:
            raise ValueError('invalid key signature')


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
