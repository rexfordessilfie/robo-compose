import time
from tone import Tone
from chords import ChordFactory, ChordQuality
from intervals import EqualTemperament12, sharpen, flatten
from pitches import Pitch, KeySignature
from notes import Note, TimeSignature, NoteValue
from scales import ScaleMode
from utils import filename_timestamp


def rest(duration=0.005):
    time.sleep(duration)


def slider_song(bars=2):
    chord = ChordFactory.get_chord(440, 'MM7M6')
    progression = [chord,
                   list(map(sharpen, chord)),
                   list(map(flatten, chord)),
                   list(map(flatten, chord)),
                   list(map(flatten, chord)),
                   list(map(flatten, chord))]

    for _ in range(bars):
        Tone.play_progression(progression)
        rest(0.005)


def summer_fun_song(bars=2):
    chord1 = ChordFactory.get_chord(440, ChordQuality.MAJOR)
    chord2 = ChordFactory.get_chord(440 * EqualTemperament12.PERFECT_FOURTH, ChordQuality.MAJOR)
    chord3 = ChordFactory.get_chord(440 * EqualTemperament12.PERFECT_FIFTH, ChordQuality.MAJOR)

    progression = [chord1,
                   chord1,
                   chord2,
                   chord3]

    for _ in range(bars):
        Tone.play_progression(progression)
        rest(0.005)


def random_song(bars=2,
                mode=ScaleMode.MAJOR,
                root_frequency=440,
                num_notes=8):
    key_signature = KeySignature(pitch=Pitch(root_frequency), mode=mode)
    random_notes = [
        Note.random(key_signature=key_signature)
        for _ in range(num_notes)]

    timestamp = filename_timestamp()
    Tone.write_wav_melody(f"random_song{timestamp}.wav", random_notes)
    Tone.write_midi_melody(f"random_song{timestamp}.mid", random_notes)

    for _ in range(bars):
        Tone.play_melody(random_notes)
        rest(0.005)


def scale_song(bars=2,
               mode=ScaleMode.MAJOR,
               root_frequency=440):
    scale = KeySignature(pitch=Pitch(root_frequency), mode=mode).scale

    for _ in range(bars):
        Tone.play_melody(scale)
        rest(0.005)


def random_piece(bars=2,
                 mode=ScaleMode.MAJOR,
                 root_frequency=440,
                 num_notes=12,
                 bpm=80):
    root_pitch = Pitch(root_frequency)
    key_signature = KeySignature(pitch=root_pitch, mode=mode)
    time_signature = TimeSignature(4, NoteValue.QUARTER)

    random_notes = [
        Note.random(key_signature=key_signature, time_signature=time_signature, bpm=bpm)
        for _ in range(num_notes)]

    timestamp = filename_timestamp()
    Tone.write_wav_melody(f"random_piece{timestamp}.wav", random_notes)
    Tone.write_midi_melody(f"random_piece{timestamp}.mid", random_notes)

    for _ in range(bars):
        Tone.play_melody(random_notes)
        rest(0.005)


if __name__ == '__main__':
    random_song()
    pass
