from typing import List, Union
from composer.notes import Note, Duration
from composer.pitches import Pitch

from synthesizer import Player, Synthesizer, Waveform


class Tone:
    player = Player()
    synthesizer = Synthesizer(osc1_waveform=Waveform.triangle,
                              osc1_volume=1.0, use_osc2=False)

    is_stream_open = False

    @classmethod
    def ensure_stream_open(cls):
        if not cls.is_stream_open:
            cls.player.open_stream()
            cls.is_stream_open = True

    # TODO: move these to an outside utility file?
    @classmethod
    def get_frequency(cls, o: Union[float, Pitch, Note]):
        return o if isinstance(o, float) or isinstance(o, int) \
            else o.frequency if isinstance(o, Pitch) \
            else o.pitch.frequency if isinstance(o, Note) \
            else None

    @classmethod
    def get_duration(cls, o: object, default: float = None):
        return o.duration.value if isinstance(o, Note) \
            else o.value if isinstance(o, Duration) \
            else default

    @classmethod
    def play_note(cls, note: Union[float, Pitch, Note] = None, duration: float = 1):
        _frequency = cls.get_frequency(note)
        _duration = cls.get_duration(note, duration)

        wave = cls.synthesizer.generate_constant_wave(_frequency, _duration)

        cls.ensure_stream_open()
        cls.player.play_wave(wave)

    @classmethod
    def play_chord(cls, chord: List[Union[float, Pitch, Note]] = None, duration: float = 1):
        _frequencies = [cls.get_frequency(note) for note in chord]

        wave = cls.synthesizer.generate_chord(_frequencies, duration)

        cls.ensure_stream_open()
        cls.player.play_wave(wave)

    @classmethod
    def play_melody(cls, notes: List[Union[float, Pitch]] = None, duration: float = 1):
        _frequencies = [cls.get_frequency(note) for note in notes]
        _durations = [cls.get_duration(note, duration) for note in notes]

        for i in range(len(notes)):
            cls.play_note(_frequencies[i], _durations[i])

    @classmethod
    def play_progression(cls, chords: List[List[Union[float, Pitch]]] = None, duration: float = 1):
        for i in range(len(chords)):
            cls.play_chord(chords[i])
