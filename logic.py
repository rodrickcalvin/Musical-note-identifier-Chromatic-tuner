# =================================================================
# The Note values are midi note Number
# Advice to keep Frame_Size and Frames_per_FFT to be powers of two.
class TunerLogic:
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

