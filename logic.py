import numpy as np
# import frequencies


# =================================================================================================
# The Note values are midi note Number
# Advice to keep Frame_Size and Frames_per_FFT to be powers of two.
class TunerLogic:

    Sampling_Freq = 22050  # Sampling frequency in Hz
    Frame_Size = 2048  # How many samples per frame?
    RECORDING_TIME = 3             # time to record audio
    Frames_per_FFT = 16  # FFT takes average across how many frames?
    Standard_Freq = 440.0

    def __init__(self, instrument):
        # BASS GUITAR
        if instrument == "Bass Guitar":
            self.Note_min = 23              # B0
            self.Note_max = 48              # C3

        # ACOUSTIC/ELECTRIC GUITAR
        if instrument == "Acoustic/Electric Guitar":
            self.Note_min = 40              # E2
            self.Note_max = 64              # E4

        # UKULELE
        if instrument == "Ukulele":
            self.Note_min = 60              # C4
            self.Note_max = 69              # A4


        ######################################################################
        # Derived quantities from constants above. Note that as
        # Samples_per_FFT goes up, the frequency step size decreases (so
        # resolution increases); however, it will incur more delay to process
        # new sounds.

        self.Samples_per_FFT = self.Frame_Size * self.Frames_per_FFT
        self.FREQ_STEP = float(self.Sampling_Freq)/self.Samples_per_FFT

        ######################################################################
        # For printing out notes

        self.NOTE_NAMES = 'C C#/Db D D#/Eb E F F# G G#/Ab A A#/Bb B'.split()

        ######################################################################
        self.num_frames = 0

    def freq_to_midi(self, f):
        return 69 + 12 * np.log2(f / self.Standard_Freq)

    def midi_to_freq(self, n):
        return int(self.Standard_Freq) * 2.0 ** ((n - 69) / 12.0)

    def note_name(self, n):
        return self.NOTE_NAMES[n % 12] + str(n / 12 - 1)

    ######################################################################
    # Get min/max index within FFT of notes we care about.
    # See docs for numpy.rfftfreq()
    def note_to_fftbin(self, n):
        return self.midi_to_freq(n) / self.FREQ_STEP

    def get_imin(self):
        self.imin = max(0, int(np.floor(self.note_to_fftbin(self.Note_min - 1))))
        return self.imin

    def get_imax(self):
        self.imax = min(self.Samples_per_FFT, int(np.ceil(self.note_to_fftbin(self.Note_max + 1))))
        return self.imax

    # Allocate space to run an FFT.
    def get_buffer(self):
        self.buf = np.zeros(self.Samples_per_FFT, dtype=np.float32)
        return self.buf

# create an instance
# t =  TunerLogic()

