from typing import List, Union
from notes import Note, Duration, TimeSignature, NoteValue
from pitches import Pitch
from utils import filename_timestamp

from synthesizer import Player, Synthesizer, Waveform, Writer
import numpy as np
import os

from midiutil import MIDIFile

# TODO: extend this class and make it subclass-able. Each will be instantiated with an instrument name/waveform
#   This way we can have something like PianoTone = Tone(instrument='piano'), etc, and then
#   the class will instantiate a synthesizer that uses a piano tone.
# TODO: move these to an outside utility file?

OUT_DIR = "out"
WAV_OUT_DIR = f"{OUT_DIR}/wav"
MIDI_OUT_DIR = f"{OUT_DIR}/midi"


def extract_frequency(o: Union[float, Pitch, Note]):
    return o if isinstance(o, float) or isinstance(o, int) \
        else o.frequency if isinstance(o, Pitch) \
        else o.pitch.frequency if isinstance(o, Note) \
        else None


def extract_duration(o: Union[float, Duration, Note], default: float = None):
    return o.duration.value if isinstance(o, Note) \
        else o.value if isinstance(o, Duration) \
        else default


def ensure_out_directory_exists(directory: str):
    if not os.path.exists(f"../{directory}"):
        os.makedirs(f"../{directory}")


def wav_out_file_path(filename: str):
    ensure_out_directory_exists(WAV_OUT_DIR)
    return f"../{WAV_OUT_DIR}/{filename}"


def midi_out_file_path(filename: str):
    ensure_out_directory_exists(MIDI_OUT_DIR)
    return f"../{MIDI_OUT_DIR}/{filename}"


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
    def write_wav_melody(cls, filename: str, notes: List[Union[float, Pitch, Note]] = None, duration: float = 1):
        file_path = wav_out_file_path(filename)
        melody_wav = np.concatenate([cls.wave_from_note(note, duration) for note in notes])
        cls.writer.write_wave(file_path, melody_wav)

    @classmethod
    def write_wav_progression(cls, filename: str, chords: List[List[Union[float, Pitch, Note]]] = None,
                              duration: float = 1):
        file_path = wav_out_file_path(filename)
        progression_wav = np.concatenate([cls.wave_from_chord(chord, duration) for chord in chords])
        cls.writer.write_wave(file_path, progression_wav)

    @classmethod
    def write_midi_melody(cls, filename: str, notes: List[Union[float, Pitch, Note]], duration: float = 1):
        volume = 110  # range: 0-127
        melody_track = 0
        melody_channel = 0

        # TODO: have a Song object, on which we can attach time_signature and bpm information for a song
        #  and then extract for use here. Durations already provide the absolute value of time for us.

        midi = MIDIFile(numTracks=1)

        time_marker = 0
        for note in notes:
            _duration = extract_duration(note, duration)
            _pitch = int(note.pitch.midi_number)

            if note.duration.bpm:
                # TODO: debug whether this has any effect on output midi file
                midi.addTempo(track=melody_track, time=time_marker, tempo=note.duration.bpm)

            midi.addNote(track=melody_track,
                         time=time_marker,
                         pitch=_pitch,
                         duration=_duration,
                         volume=volume,
                         channel=melody_channel)

            time_marker = time_marker + note.duration.value

        filepath = midi_out_file_path(filename)

        with open(filepath, "wb") as output_file:
            midi.writeFile(output_file)


if __name__ == '__main__':
    time_signature = TimeSignature(num_beats=2, note_value=NoteValue.QUARTER)
    melody = [Note.random(time_signature=time_signature, bpm=60),
              Note.random(time_signature=time_signature, bpm=80),
              Note.random(time_signature=time_signature, bpm=120)]

    timestamp = filename_timestamp()
    Tone.play_melody(melody)
    Tone.write_midi_melody(f'test{timestamp}.mid', melody)
    Tone.write_wav_melody(f'test{timestamp}.wav', melody)
