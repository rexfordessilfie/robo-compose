import math
import scales
import random


class KeySignature:
    def __init__(self, pitch, mode):
        self.pitch = pitch
        self.mode = mode

    def get_scale(self):
        scale_factory = scales.ScaleFactory()
        scale_pitches = scale_factory.get_scale(self.pitch.get_frequency(),
                                                self.mode)
        return scale_pitches


class Pitch:
    def __init__(
            self,
            frequency=0,
            pitch_class='',
            accidental='natural',
            register=-1):
        '''TODO: be able to derive a pitch name from its frequency and vice versa'''
        self.frequency = frequency

    def __str__(self):
        return f"Pitch: {self.frequency}"
        # return f"{self.pitch_class}{self.accidental}{self.register}({self.frequency})"

    def get_frequency(self):
        return self.frequency

    @staticmethod
    def get_pitch_info_from_frequency(frequency):
        '''TODO: get pitch info as dictionary {pitch_class: 'A', accidental: 'natural', register: 5 } '''
        pass

    @staticmethod
    def determine_frequency_from_pitch_info(pitch_class, accidental, register):
        '''TODO: get frequency as number from the pitch information '''
        pass

    @staticmethod
    def get_random(key=None):
        if key and isinstance(key, KeySignature):
            scale = key.get_scale()
            random_index = random.randrange(0, len(scale))
            return scale[random_index]
        else:
            print('Key Signature is invalid')


class Duration:
    def __init__(self, seconds=0, note_value=None):
        self.duration = seconds
        self.note_value = note_value

    @staticmethod
    def get_random(max_duration=math.inf, quantized=False, bpm=None):
        '''TODO: get a random duration and return it. If quantized then return something that aligns to a specific division of the beat or bpm. Consider time signature??'''
        pass


class Note:
    def __init__(self, pitch=None, duration=None):
        self.pitch = pitch
        self.duration = duration

    def get_frequency(self):
        return self.pitch.get_frequency()

    def get_duration(self):
        return self.pitch.get_duration()

    @staticmethod
    def get_random(max_duration=math.inf, quantized=False, bpm=None, key=None):
        new_pitch = Pitch.get_random(key)
        new_duration = Duration.get_random(max_duration=max_duration,
                                           quantized=quantized,
                                           bpm=bpm)
        return Note(new_pitch, new_duration)
