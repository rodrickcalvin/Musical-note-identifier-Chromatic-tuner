import numpy as np
import pyaudio
import wave

FSAMP = 44100       # Sampling frequency in Hz
FRAME_SIZE = 1024   # How many samples per frame?
# time to record audio
RECORDING_TIME = input(
    "For how long would you like your recording to run? (seconds)")
WAVE_OUTPUT = input("What is the name of the file to store your recording?")


def main():
    create = open((WAVE_OUTPUT+".wav"), "w+")

main()
WAVE_OUTPUT = WAVE_OUTPUT+".wav"

stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                channels=2,
                                rate=FSAMP,
                                input=True,
                                frames_per_buffer=FRAME_SIZE)

print("recording......")

frames = []

for x in range(0, int(FSAMP/FRAME_SIZE*int(RECORDING_TIME))):
    data = stream.read(FRAME_SIZE)
    frames.append(data)

print("finished recording......")

# close recorder
stream.stop_stream()
stream.close()

# Save file into a 'wav format
wavFile = wave.open(WAVE_OUTPUT, 'wb')
wavFile.setnchannels(2)
wavFile.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
wavFile.setframerate(FSAMP)
wavFile.writeframes(b''.join(frames))
wavFile.close()
