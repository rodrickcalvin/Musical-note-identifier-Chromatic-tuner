import pyaudio
import numpy as np
import frequencies
from GUI import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

instrument = "Bass guitar"
# =================================================================================================
# The Note values are midi note Number
# Advice to keep FRAME_SIZE and FRAMES_PER_FFT to be powers of two.
class Tuner():
    def __init__(self, instrument):
        # BASS GUITAR
        if instrument == "Bass guitar":
            self.NOTE_MIN = 23       # B0
            self.NOTE_MAX = 48       # 
        
        # ACOUSTIC/ELECTRIC GUITAR
        if instrument == "Acoustic/Electric guitar":
            self.NOTE_MIN = 40       # E2
            self.NOTE_MAX = 64       # E4
        
        # UKELELE
        if instrument == "ukelele":
            self.NOTE_MIN = 60       # C4
            self.NOTE_MAX = 69       # A4

        # super().__init__()
        # self.ui = Ui_Dialog()
        # self.ui.setupUi(self)



# create an instance
t = Tuner(instrument)


FSAMP = 22050      # Sampling frequency in Hz
FRAME_SIZE = 2048   # How many samples per frame?
RECORDING_TIME = 3  # time to record audio
FRAMES_PER_FFT = 16 # FFT takes average across how many frames?

######################################################################
# Derived quantities from constants above. Note that as
# SAMPLES_PER_FFT goes up, the frequency step size decreases (so
# resolution increases); however, it will incur more delay to process
# new sounds.

SAMPLES_PER_FFT = FRAME_SIZE*FRAMES_PER_FFT
FREQ_STEP = float(FSAMP)/SAMPLES_PER_FFT

######################################################################
# For printing out notes

NOTE_NAMES = 'C C#/Db D D#/Eb E F F# G G#/Ab A A#/Bb B'.split()

######################################################################

def freq_to_midi(f): return 69 + 12*np.log2(f/440.0)
def midi_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n): return NOTE_NAMES[n % 12] + str(n/12 - 1)

######################################################################
# Ok, ready to go now.

# Get min/max index within FFT of notes we care about.
# See docs for numpy.rfftfreq()
def note_to_fftbin(n): return midi_to_freq(n)/FREQ_STEP
imin = max(0, int(np.floor(note_to_fftbin(t.NOTE_MIN-1))))
imax = min(SAMPLES_PER_FFT, int(np.ceil(note_to_fftbin(t.NOTE_MAX+1))))

# Allocate space to run an FFT. 
buf = np.zeros(SAMPLES_PER_FFT, dtype=np.float32)
num_frames = 0

# Initialize audio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=FSAMP,
                input=True,
                frames_per_buffer=FRAME_SIZE)

stream.start_stream()

# Create Hanning window function
window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, SAMPLES_PER_FFT, False)))

# Print initial text
print('sampling at', FSAMP, 'Hz with max resolution of', FREQ_STEP, 'Hz')

# As long as we are getting data:
while stream.is_active():

    # Shift the buffer down and new data in
    buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
    buf[-FRAME_SIZE:] = np.fromstring(stream.read(FRAME_SIZE), np.int16)

    # Run the FFT on the windowed buffer
    fft = np.fft.rfft(buf * window)

    # Get frequency of maximum response in range
    freq = (np.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

    # Get note number and nearest note
    n = freq_to_midi(freq)
    n0 = int(round(n))

    # Console output once we have a full buffer
    num_frames += 1

    if num_frames >= FRAMES_PER_FFT:
        print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(
            freq, note_name(n0), n-n0))
