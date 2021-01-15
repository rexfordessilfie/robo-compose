from intervals import EqualTemperament as et
import scales
import math

tuning = {"A440": 440}

## steps: get the frequency, divide by 440 and then determine what interval it is by comparing result to possible interval values
## after determining the interval, we can figure out the note is

A4 = 440
C5 = A4 * et.MINOR_THIRD.value

sample_pitch = 880
print(f"Candidate {sample_pitch}")

c_chromatic_scale = scales.ScaleFactory().get_scale(C5, "chromatic")
print(f"C chromatic scale {c_chromatic_scale}")


quotient = sample_pitch/A4

## Need to figure out how to get a pitch name from frequency (western music system)
for freq in c_chromatic_scale:
    division_result = freq/sample_pitch
    floored_result = math.floor(division_result)

    if division_result == floored_result:
        print("found")