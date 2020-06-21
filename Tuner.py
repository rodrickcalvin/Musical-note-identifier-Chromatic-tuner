import sys
import pyaudio
from PyQt5.QtWidgets import QDialog, QApplication
from GUI import *
from logic import *







class GuitarTuner(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.startBtn_3.clicked.connect(lambda: self.setKey("ee"))
        self.ui.startBtn_3.clicked.connect(lambda: self.setFrequency("1000 Hz"))
        self.ui.startBtn_3.clicked.connect(lambda: self.setLeftPercentageBar(100))
        self.ui.instrumentChooserComboxBox_3.currentIndexChanged.connect(
            lambda: self.setFrequency(self.ui.instrumentChooserComboxBox_3.currentText()))
        self.show()

    def setKey(self, key):
        self.ui.curentKeyLabel_3.setText(str(key))

    def setFrequency(self, freq):
        self.ui.frequencyLabel_3.setText(str(freq))

    def setLeftPercentageBar(self, val):
        self.ui.levelLeft_Progress_3.setProperty("value", val)

    def setRightPercentageBar(self, val):
        self.ui.levelRight_Progress_3.setProperty("value", val)

    def setPercentageBars(self, leftValue, rightValue):
        self.ui.levelLeft_Progress_3.setProperty("value", leftValue)
        self.ui.levelRight_Progress_3.setProperty("value", rightValue)


    def getInstrument(self):
        instrument = str(self.ui.instrumentChooserComboxBox_3.currentText())
        return instrument




if __name__ == "__main__":
    app = QApplication(sys.argv)
    windowx = GuitarTuner()
    t = TunerLogic(windowx.getInstrument())
    windowx.setFrequency(str(t.Note_min))

    # Initialize audio
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                    channels=1,
                    rate=t.Sampling_Freq,
                    input=True,
                    frames_per_buffer=t.Frame_Size)

    stream.start_stream()

    # Create Hanning window function
    window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, t.Samples_per_FFT, False)))

    # Print initial text
    print('sampling at', t.Sampling_Freq, 'Hz with max resolution of', t.FREQ_STEP, 'Hz')
    #
    # As long as we are getting data:
    while stream.is_active():
        # Shift the buffer down and new data in
        t.get_buffer()[:-t.Frame_Size] = t.get_buffer()[t.Frame_Size:]
        t.get_buffer()[-t.Frame_Size:] = np.fromstring(stream.read(t.Frame_Size), np.int16)

        # Run the FFT on the windowed buffer
        fft = np.fft.rfft(t.get_buffer() * window)

        # Get frequency of maximum response in range
        freq = (np.abs(fft[t.get_imin():t.get_imax()]).argmax() + t.get_imin()) * t.FREQ_STEP

        # Get note number and nearest note
        n = t.freq_to_midi(freq)
        n0 = int(round(n))

        # Console output once we have a full buffer
        t.num_frames += 1

        if t.num_frames >= t.Frames_per_FFT:
            print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(
                freq, t.note_name(n0), n-n0))

            windowx.show()
            # sys.exit(app.exec_())








    # windowx.show()
    # sys.exit(app.exec_())
