# robo-compose
Robo-compose is a fun Python project for creating random melodies for compositional inspiration. 
Robo-compose also contains some utility classes and functions that model musical concepts in an object-oriented style, 
and allow for musical programming.

# Definitions
The `composer` package contains the following classes:
* `Pitch`: This is a sound identified by a frequency e.g. `440Hz`, `466Hz`, or 
by a note name - referred to as "pitch string" - e.g. `'A4'`, `'A4#'`.
* `Note`: This is a sound identified by a `Pitch` and a `Duration`.
* `Duration`: This is a length of time identified explicitly by time in seconds, 
or relatively by a combination of a `NoteValue`, bpm, and a `TimeSignature`.
* `NoteValue`: This is a Western music note value identified by a number (or fraction). 
Note values include, whole note (1), half note (1/2), quarter note (1/4) etc.
* `TimeSignature`: This is a Western music time signature identified by a combination of
number of beats and the note value of a beat.
* `Interval`: a number denoting the relative distance between two frequencies. Common intervals in Western
Music include, the perfect fifth (3/2), octave (2/1) and more.
* `Temperament`: This a Western Music tuning system identified by a list of intervals.
Examples include equal temperament, and just-intonation.
* `Scale` (or `Chord`): This is an arbitrary collection of intervals that identify a given scale (or chord).


# Usage
### `Pitch`
**Instantiation**

A `Pitch` may be instantiated as follows:
```python
from composer import Pitch, PitchClass, Accidental

# Instantiation
a4 = Pitch(440)

g4_flat = Pitch("G4b")

c5_sharp = Pitch(pitch_class=PitchClass.C, accidental=Accidental.SHARP, register=5)
```
When a `Pitch` is created, the details on the `pitch_class`, `accidental`, `register`, `enharmonic_pitch_class`
and `enharmonic_accidental` are automatically discovered and set on the object if not provided.

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
assert duration_3_seconds == 3 # True
assert duration_for_quarter_note == 1 # True
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

### Play Audio w/ `Tone`
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
```
