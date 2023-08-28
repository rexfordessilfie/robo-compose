# robo-compose
RoboCompose is a fun Python project for creating random melodies for compositional inspiration.
RoboCompose also contains some utility classes and functions that model musical concepts,
and allow for musical programming.

This project was inspired by a desire to create musical ideas, and to practice design patterns and OOP in Python.


# Demo
Follow these steps to try out this project:

1. Clone the repository and then change into the project directory:
    ```shell
    $ git clone https://github.com/RexfordEssilfie/robo-compose.git
    $ cd robo-compose 
    ```

2. Install requirements using:
    ```shell
    $ pip install -r requirements.txt
    ```

    NB: You will need to install Python 3.9.1 first from [here](https://www.python.org/downloads/).

3. Open `composer/songs.py` file, where you will find functions representing songs,
such as, `random_song()`, `summer_fun_song()` and more.

4. Add a call to the song's function in the main method of the file as follows:
    ```python
    # composer/songs.py

    def random_song():
      ...


    if __name__ == "__main__":
        random_song() # Call the function here!
        pass
    ```

     The `random_song` function will play a randomly generated song, and write midi and wav files to the `out` directory, in case you want
  to come back to them for later or open in MuseScore or Logic Pro X for further exploration and development!

6. Run the `composer/songs.py` file to play the song, using the following command:
    ```shell
    $ python composer/songs.py
    ```



# Usage
### `Pitch`
**Instantiation**

A `Pitch` may be instantiated as follows:
```python
from composer import Pitch, PitchClass, Accidental

# Instantiation from Frequency
a4 = Pitch(440)

# Instantiation from Pitch String
g4_flat = Pitch("G4b")

# Instantiation from MIDI Number
c5 = Pitch(midi_number=60)

# Instantiation from Pitch Information
c5_sharp = Pitch(pitch_class=PitchClass.C, accidental=Accidental.SHARP, register=5)


# Pitch Information
print(c5_sharp.frequency)                 # 554.36
print(c5_sharp.midi_number)               # 73
print(c5_sharp.register)                  # 5
print(c5_sharp.pitch_class)               # "C"
print(c5_sharp.accidental)                # "sharp"
print(c5_sharp.enharmonic_pitch_class)    # "D"
print(c5_sharp.enharmonic_accidental)     # "flat"
```
When a `Pitch` is instantiated, the details of it's `pitch_class`, `accidental`, `register`, `enharmonic_pitch_class`
and `enharmonic_accidental` are automatically inferred and set on the object if not provided. 

The order of what is used to determine the `Pitch` is first the `identifier` (i.e frequency or pitch string), then the `midi_number`, and then combination of `pitch_class`, `accidental` and `register`.

Finally, the format for a pitch string is the [Scientific Pitch Notation](https://en.wikipedia.org/wiki/Scientific_pitch_notation), i.e. the pitch class (e.g. "A", "B", "C", ..., "G") + accidental ("#" or "b" if needed) + register (a non-negative integer)


**Functions**

```python
from composer import Pitch, KeySignature, ScaleMode

a4 = Pitch(440)
a8 = Pitch("A8")

# Pitch Matching (same pitch class and accidental)
assert a4.matches(a8)

# Cycling through Pitches
g4_sharp = a4.prev()
a4_sharp = a4.next()

# Generating a Random Pitch!
scale_random_pitch = Pitch.random(key_signature=KeySignature(a4, ScaleMode.CHROMATIC))
completely_random_pitch = Pitch.random()
```

### `Duration`

**Instantiation**

A `Duration` may be instantiated as follows:
```python
from composer import Duration, TimeSignature, NoteValue

# Create a Duration of 3 seconds
duration_3_seconds = Duration(3)

# Create a Duration from bpm, time_signature and more
time_signature_4_4 = TimeSignature(4, NoteValue.QUARTER)
duration_for_quarter_note = Duration(note_value=NoteValue.QUARTER,
                                     time_signature=time_signature_4_4,
                                     bpm=60)

# Access Duration in seconds
assert duration_3_seconds.value == 3 # True
assert duration_for_quarter_note.value == 1 # True
```
After a `Duration` has been created, the raw time value in seconds can be obtained by accessing `.value` property.
Future work may add support to normalize a duration in seconds to a Western music note value equivalent.

**Functions**

```python
from composer import Duration, TimeSignature, NoteValue

# Generate a Random Duration that is a fraction of 2 seconds.
random_duration = Duration.random(factor=2)

# Generate a Random (Western music) Duration
time_signature_4_4 = TimeSignature(4, NoteValue.QUARTER)
random_duration_2 = Duration.random(bpm=60, time_signature=time_signature_4_4)
```

### `Note`
This is mainly a convenience class that groups `Pitch` and `Duration` objects into one object.

**Instantiation**

A `Note` may be instantiated as follows:
```python
from composer import Note, Pitch, Duration

# Create a 3-second note on A4 pitch
my_note = Note(pitch=Pitch(440), duration=Duration(3))
```
When a `Note` is created, all the pitch and duration information are accessible on the `.pitch` and `.duration` properties.

**Functions**

```python
from composer import Note

# Create a Random Note
random_note = Note.random()
```

### Play/Save Audio w/ `Tone`
To play notes, you can use the `Tone` class defined in `composeer.tone` (`tone.py`).
This class is a simple one that provides functions for playing a single note, melody, or chord.

Sample songs have been defined in `composer.songs` (`songs.py`) that contain sample usages of `Tone`.

**Example:**

```python
from composer import Note, Tone, Pitch, ScaleMode, ChordFactory, ScaleFactory

# Play a Note
note = Note.random()
Tone.play_note(note)

# Play a Scale (C5# major scale)
melody = ScaleFactory.get_scale(Pitch("C5#").frequency, mode=ScaleMode.MAJOR)
Tone.play_melody(melody)

# Play a Chord (C5# Major 7 chord)
chord = ChordFactory.get_chord(Pitch("C5#").frequency, "MM7")
Tone.play_chord(chord)

# Save Melody as WAV
Tone.write_wav_melody("my_melody.wav", melody)

# Save Melody as MIDI
Tone.write_midi_melody("my_melody.mid", melody)
```

# Definitions
The `composer` package contains the following classes:
* `Pitch`: This is a sound identified by a frequency e.g. `440Hz`, `466Hz`, or
  by a note name - referred to as "pitch string" - e.g. `"A4"`, `"A4#"`.
* `Note`: This is a sound identified by a `Pitch` and a `Duration`.
* `Duration`: This is a length of time identified explicitly by time in seconds,
  or relatively by a combination of a `NoteValue`, bpm, and a `TimeSignature`.
* `NoteValue`: This is a Western music note value identified by a number (or fraction).
  Note values include, whole note (1), half note (1/2), quarter note (1/4) etc.
* `TimeSignature`: This is a Western music time signature identified by a combination of
  number of beats and the note value of a beat.
* `Interval`: A number denoting the relative distance between two frequencies. Common intervals in Western
  Music include, the perfect fifth (3/2), octave (2/1) and more.
* `Temperament`: This a Western Music tuning system identified by a list of intervals.
  Examples include equal temperament, and just-intonation.
* `Scale` (or `Chord`): This is an arbitrary collection of intervals that identify a given scale (or chord).

# Future Work
I plan on working on some more features to add to this project to make it more useful for composition and musical programming. Some ideas include:
1. Generating random chord progressions
2. Heuristic/probabilistic-based random melodies
3. Improve modeling for songs/pieces for multi-part composition
4. Harmonic analysis!

Ideas and feature requests are welcome!
