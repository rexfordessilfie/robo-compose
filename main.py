from composer.tone import Tone
from composer.pitches import Pitch, KeySignature
from composer.notes import Note
from composer.scales import ScaleMode
from composer.utils import filename_timestamp

BARS = 4
ROOT_FREQUENCY = 440
MODE = ScaleMode.CHROMATIC
NOTE_COUNT = 12

if __name__=="__main__":
    print("Composing song..")
    key_signature = KeySignature(pitch=Pitch(ROOT_FREQUENCY), mode=MODE)
    random_notes = [
        Note.random(key_signature=key_signature)
        for _ in range(NOTE_COUNT)]

    timestamp = filename_timestamp()

    print("Saving song..")
    Tone.write_wav_melody(f"my-song{timestamp}.wav", random_notes)
    Tone.write_midi_melody(f"my-song{timestamp}.mid", random_notes)

    print("Playing song..")
    for _ in range(BARS):
        Tone.play_melody(random_notes)
        Tone.rest(0.005)


