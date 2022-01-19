from typing import List, Union
from composer.notes import Note, Duration
from composer.pitches import Pitch

from synthesizer import Player, Synthesizer, Waveform, Writer
import numpy as np
import os

# TODO: extend this class and make it subclass-able. Each will be instantiated with an instrument name/waveform
#   This way we can have something like PianoTone = Tone(instrument='piano'), etc, and then
#   the class will instantiate a synthesizer that uses a piano tone.
# TODO: move these to an outside utility file?

WAV_OUT_DIR = 'waves'


def extract_frequency(o: Union[float, Pitch, Note]):
    return o if isinstance(o, float) or isinstance(o, int) \
        else o.frequency if isinstance(o, Pitch) \
        else o.pitch.frequency if isinstance(o, Note) \
        else None


def extract_duration(o: Union[float, Duration, Note], default: float = None):
    return o.duration.value if isinstance(o, Note) \
        else o.value if isinstance(o, Duration) \
        else default


def ensure_wav_directory_exists():
    if not os.path.exists(f'../{WAV_OUT_DIR}'):
        os.makedirs(f'../{WAV_OUT_DIR}')


def wav_file_path(filename: str):
    ensure_wav_directory_exists()
    return f"../{WAV_OUT_DIR}/{filename}"


class Tone:
    player = Player()
    synthesizer = Synthesizer(osc1_waveform=Waveform.triangle,
                              osc1_volume=1.0, use_osc2=False)
    writer = Writer()

    is_stream_open = False

    @classmethod
    def _ensure_stream_open(cls):
        if not cls.is_stream_open:
            cls.player.open_stream()
            cls.is_stream_open = True

    @classmethod
    def wave_from_note(cls, note: Union[float, Pitch, Note] = None, duration: float = 1):
        _frequency = extract_frequency(note)
        _duration = extract_duration(note, duration)
        return cls.synthesizer.generate_constant_wave(_frequency, _duration)

    @classmethod
    def wave_from_chord(cls, chord: List[Union[float, Pitch, Note]] = None, duration: float = 1):
        _frequencies = [extract_frequency(note) for note in chord]
        return cls.synthesizer.generate_chord(_frequencies, duration)

    @classmethod
    def play_note(cls, note: Union[float, Pitch, Note] = None, duration: float = 1):
        wave = cls.wave_from_note(note, duration)
        cls._ensure_stream_open()
        cls.player.play_wave(wave)

    @classmethod
    def play_chord(cls, chord: List[Union[float, Pitch, Note]] = None, duration: float = 1):
        wave = cls.wave_from_chord(chord, duration)
        cls._ensure_stream_open()
        cls.player.play_wave(wave)

    @classmethod
    def play_melody(cls, notes: List[Union[float, Pitch, Note]] = None, duration: float = 1):
        for note in notes:
            cls.play_note(note, duration)

    @classmethod
    def play_progression(cls, chords: List[List[Union[float, Pitch, Note]]] = None, duration: float = 1):
        for chord in chords:
            cls.play_chord(chord, duration)

    @classmethod
    def write_melody(cls, filename: str, notes: List[Union[float, Pitch, Note]] = None, duration: float = 1):
        file_path = wav_file_path(filename)
        melody_wav = np.concatenate([cls.wave_from_note(note, duration) for note in notes])
        cls.writer.write_wave(file_path, melody_wav)

    @classmethod
    def write_progression(cls, filename: str, chords: List[List[Union[float, Pitch, Note]]] = None,
                          duration: float = 1):
        file_path = wav_file_path(filename)
        progression_wav = np.concatenate([cls.wave_from_chord(chord, duration) for chord in chords])
        cls.writer.write_wave(file_path, progression_wav)
