import time
from composer.tone import Tone
from composer.chords import ChordFactory, ChordQuality
from composer.intervals import EqualTemperament, sharpen, flatten
from composer.pitches import Pitch, KeySignature
from composer.notes import Note, TimeSignature, NoteValue
from composer.scales import ScaleMode


def rest(duration=0.005):
    time.sleep(duration)


def slider_song(bars=4):
    chord = ChordFactory.get_chord(440, 'MM7M6')
    for _ in range(bars):
        Tone.play_progression(
            [chord,
             map(sharpen, chord),
             map(flatten, chord),
             map(flatten, chord),
             map(flatten, chord),
             map(flatten, chord)])
        rest(0.005)


def summer_fun_song(bars=4):
    chord1 = ChordFactory.get_chord(440, ChordQuality.MAJOR)
    chord2 = ChordFactory.get_chord(440 * EqualTemperament.PERFECT_FOURTH, ChordQuality.MAJOR)
    chord3 = ChordFactory.get_chord(440 * EqualTemperament.PERFECT_FIFTH, ChordQuality.MAJOR)

    for _ in range(bars):
        Tone.play_progression(
            [chord1,
             chord1,
             chord2,
             chord3])
        rest(0.005)


def random_song(bars=4,
                mode=ScaleMode.MAJOR,
                root_frequency=440,
                num_notes=8):

    key_signature = KeySignature(pitch=Pitch(root_frequency), mode=mode)
    random_notes = [
        Note.random(key_signature=key_signature)
        for _ in range(num_notes)]

    for _ in range(bars):
        Tone.play_melody(random_notes)
        rest(0.005)


def scale_song(bars=1,
               mode=ScaleMode.MAJOR,
               root_frequency=440):
    scale = KeySignature(pitch=Pitch(root_frequency), mode=mode).scale

    for _ in range(bars):
        Tone.play_melody(scale)
        rest(0.005)


def random_piece(bars=4,
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

    print(random_notes)

    for _ in range(bars):
        Tone.play_melody(random_notes)
        rest(0.005)


if __name__ == '__main__':
    summer_fun_song()
    pass
