import numpy
import sounddevice
import speech_recognition

MAX_INT = 32767

SAMPLE_RATE = 16000
SAMPLE_WIDTH = 2
BLOCK_SIZE = 80000

interpreter = speech_recognition.Recognizer()

def print_speech(sound_indata, frames, time, status):
    get_audio = speech_recognition.AudioData((sound_indata[:, 0]*MAX_INT).astype(numpy.int16).tobytes(), SAMPLE_RATE, SAMPLE_WIDTH)
    
    try:
        print(interpreter.recognize_google(get_audio))
    except speech_recognition.UnknownValueError:
        print("No one is speaking.")

print("Entered speaking mode. Start talking:")

with sounddevice.InputStream(callback = print_speech, channels = 1, samplerate = SAMPLE_RATE, blocksize = BLOCK_SIZE):
    while True:
        pass