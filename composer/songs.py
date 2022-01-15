
import time
from composer.tone import Tone
from composer.chords import ChordFactory
from composer.intervals import EqualTemperament
from composer.main import Note
from composer.pitches import Pitch, KeySignature


def rest(duration=0.005):
    time.sleep(duration)


def slider_song(bars=4):
    chord = ChordFactory.get_chord(440, 'MM7M6')
    for _ in range(bars):
        Tone.play_progression(
            [chord,
             map(EqualTemperament.sharpen, chord),
             map(EqualTemperament.flatten, chord),
             map(EqualTemperament.flatten, chord),
             map(EqualTemperament.flatten, chord),
             map(EqualTemperament.flatten, chord)])
        rest(0.005)


def summer_fun_song(bars=4):
    chord1 = ChordFactory.get_chord(440, 'M')
    chord2 = ChordFactory.get_chord(440 * EqualTemperament.P4, 'M')
    chord3 = ChordFactory.get_chord(440 * EqualTemperament.P5, 'M')

    for _ in range(bars):
        Tone.play_progression(
            [chord1,
             chord1,
             chord2,
             chord3])
        rest(0.005)


def random_song(bars=4,
                mode='chromatic',
                root_frequency=440,
                num_notes=8):
    random_notes = [
        Note.random(
            key=KeySignature(pitch=Pitch(frequency=root_frequency),
                             mode=mode))
        for _ in range(num_notes)]

    for _ in range(bars):
        Tone.play_melody(random_notes)
        rest()


def scale_song(bars=1,
               mode='major',
               root_frequency=440,
               ):

    scale = KeySignature(pitch=Pitch(
        frequency=root_frequency), mode=mode).get_scale()

    for _ in range(bars):
        Tone.play_melody(scale)
        rest()


if __name__ == '__main__':
    random_song()
    pass