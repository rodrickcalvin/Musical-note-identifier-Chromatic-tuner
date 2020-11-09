import numpy as np
import pyaudio


class xAudio:
    def __init__(self):
        self.count = 0
        xAudio.keyy= 0
        xAudio.freqy = 0
        xAudio.streamStatus = False
        xAudio.NOTE_MIN = 0  # C4
        xAudio.NOTE_MAX = 9000  # A4
        xAudio.FSAMP = 22050  # Sampling frequency in Hz
        xAudio.FRAME_SIZE = 2048  # How many samples per frame?
        xAudio.FRAMES_PER_FFT = 16  # FFT takes average across how many frames?
        xAudio.SAMPLES_PER_FFT = xAudio.FRAME_SIZE * xAudio.FRAMES_PER_FFT
        xAudio.FREQ_STEP = float(xAudio.FSAMP) / xAudio.SAMPLES_PER_FFT
        xAudio.NOTE_NAMES = 'C C#/Db D D#/Eb E F F# G G#/Ab A Bb B'.split()

        xAudio.imin = max(0, int(np.floor(xAudio.note_to_fftbin(xAudio.NOTE_MIN - 1))))
        xAudio.imax = min(xAudio.SAMPLES_PER_FFT, int(np.ceil(xAudio.note_to_fftbin(xAudio.NOTE_MAX + 1))))

        xAudio.buf = np.zeros(xAudio.SAMPLES_PER_FFT, dtype=np.float32)
        xAudio.num_frames = 0

        xAudio.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=xAudio.FSAMP, input=True,frames_per_buffer=xAudio.FRAME_SIZE)
        xAudio.stream.start_stream()

        xAudio.window = 0.5 * (1 - np.cos(np.linspace(0, 2 * np.pi, xAudio.SAMPLES_PER_FFT, False)))

        print('sampling at', xAudio.FSAMP, 'Hz with max resolution of', xAudio.FREQ_STEP, 'Hz')

    def freq_to_number(f):
        return 69 + 12 * np.log2(f / 440.0)

    def number_to_freq(n):
        return 440 * 2.0 ** ((n - 69) / 12.0)

    def note_name(n):
        return xAudio.NOTE_NAMES[n % 12] + str(n / 12 - 1)

    def note_to_fftbin(n):
        return xAudio.number_to_freq(n) / xAudio.FREQ_STEP

    def setNoteMinMax(self, noteMin, noteMax):
        xAudio.NOTE_MIN = noteMin
        xAudio.NOTE_MAX = noteMax

    def setStreamOff(self):
        xAudio.streamStatus = False

    def setStreamOn(self):
        xAudio.streamStatus = True

    def exitStream(self):
        xAudio.stream.stop_stream()

    def startStream(self):
        if (xAudio.streamStatus):
            xAudio.buf[:-xAudio.FRAME_SIZE] = xAudio.buf[xAudio.FRAME_SIZE:]
            xAudio.buf[-xAudio.FRAME_SIZE:] = np.fromstring(xAudio.stream.read(xAudio.FRAME_SIZE), np.int16)
            xAudio.fft = np.fft.rfft(xAudio.buf * xAudio.window)
            xAudio.freq = (np.abs(xAudio.fft[xAudio.imin:xAudio.imax]).argmax() + xAudio.imin) * xAudio.FREQ_STEP
            xAudio.n = xAudio.freq_to_number(xAudio.freq)
            xAudio.n0 = int(round(xAudio.n))
            xAudio.num_frames += 1

            if xAudio.num_frames >= xAudio.FRAMES_PER_FFT:
                print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(xAudio.freq, xAudio.note_name(xAudio.n0), xAudio.n - xAudio.n0))
                print(str(xAudio.NOTE_MIN))
                #xAudio.keyy= '{:>0.2s}'.format(xAudio.note_name(xAudio.n0))
                #xAudio.freqy= '({:7.2f} Hz)'.format(xAudio.freq) +" Note Min "+str(xAudio.NOTE_MIN)+ " Note Max" +str(xAudio.NOTE_MAX)
                xAudio.keyy= '{:>3s}'.format(xAudio.note_name(xAudio.n0))
                xAudio.freqy= '({:7.2f} Hz)'.format(xAudio.freq) +" Note Min "+str(xAudio.NOTE_MIN)+ " Note Max" +str(xAudio.NOTE_MAX)

# s = xAudio()
#s.startStream()