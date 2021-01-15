# Start of an app to generate music in python
# Gonna need some OOP maybe? 
# But for now, the main task is to be able to randomly generate a bunch of things



pitch_classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
minimum_octave = 0
maximum_octave =10
accidentals = ['flat', 'sharp', 'natural']
modes = ['major', 'minor', 'aeolian', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'locrian' ]
instruments = []
dotted = '+' #takes what was there before it and then adds half of the value to it


#Parameters to be received
tempo = 220 #in bpm
time_signature_top = 2
time_signature_bottom = [2, 4, 8, 16, 32, 64]
duration = 50 #in seconds
key_signature = 'A major' #some pitch_class and a mode
instrument = 'piano'


#computeds
'''
get_possible_notes(key)
    Have a musical definition for each of the scales

get_note_duration(bpm, note_type='quarter')
OR
get_quarter_note_duration(bpm)
'''


'''
Steps:
    While totalDuration is not reached,
        Select random pitch from available pitches
        Generate random register
        Generate random note-value or just any duration from what is left

    After song has been built, play it with some sound library
'''
#Format?: NoteWithRegister_Accidental_NoteValue OR just use frequencies + duration
song_array = ['A5_flat_quarter', 'C4_whole', 'G6_sharp_sixteenth+']



'''
OOP strategy

Classes:
 - Intervals, Scales (Modes) defined elsewhere
 - KeySignature (pitch:Pitch, scale)
        - build_scale() => Pitch[] (when initialized)
        - get_scale() => Pitch[]

 - Pitch (frequency, pitch_class, accidental, register, instrument) : takes in either pitch class or frequency and then register. If only frequency is provided, the pitch class and register can be inferred. A frequency of 0 means rest
        - get_frequency() => number
        - <static> get_random(key: KeySignature) => Pitch

 - Duration (seconds, note_value)
        - get_duration() => number
        - <static> get_random(max_duration, quantized, bpm) => Duration (if quantized, then bpm must be provided)


 - Note (pitch:Pitch, duration:Duration) : takes in a Pitch and then duration, or noteValue (that is, quarter, sixteenth, 32nd etc, eg. /1, /2, /4, /8, /16, /32+). If note value is provided, duration is computed from BPM
        - get_frequency() => pitch.get_frequency()
        - get_duration() => duration.get_duration()
        - <static> get_random(max_duration, quantized, bpm, key: KeySignature) => Note

 - Melody (total_duration, key: KeySignature, quantized, instrument)
        - generate()
        - add(note:Note)

 - Score (total_duration, quantized, instruments[])



 Scale Rules:
 major: [W, W, H...]
'''


# Possible Sound libraries: https://pypi.org/project/musicalbeeps/, https://pypi.org/project/simpleaudio/, https://earsketch.gatech.edu/earsketch2/ 