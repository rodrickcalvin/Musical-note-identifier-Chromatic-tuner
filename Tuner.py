import sys, time, asyncio
from quamash import QEventLoop
import pyaudio
from PyQt5.QtWidgets import QDialog, QApplication
from GUI import *
from logic import *




class GuitarTuner(QDialog):
    t = TunerLogic("Ukulele")

    # Initialize audio
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                    channels=1,
                    rate=t.Sampling_Freq,
                    input=True,
                    frames_per_buffer=t.Frame_Size)

    def __init__(self):
        super().__init__()
        
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # self.ui.startBtn_3.clicked.connect(lambda: self.setFrequency("1000 Hz"))
        # self.ui.startBtn_3.clicked.connect(lambda: self.setLeftPercentageBar(100))
        self.ui.startBtn_3.clicked.connect(self.invokeAsync)
        self.ui.stopBtn_3.clicked.connect(self.pauseAsync)

        self.ui.instrumentChooserComboxBox_3.currentIndexChanged.connect(
            lambda: self.setFrequency(self.ui.instrumentChooserComboxBox_3.currentText()))
        self.show()

    def invokeAsync(self):
        asyncio.ensure_future(self.updt(0.0001, self.ui.levelLeft_Progress_3, self.ui.levelRight_Progress_3, self.ui.curentKeyLabel_3, self.ui.frequencyLabel_3))
        GuitarTuner.stream.start_stream()

    def pauseAsync(self):
        # GuitarTuner.syncStatus = False
        GuitarTuner.stream.stop_stream()

    @staticmethod
    async def updt(delay, ProgressBar1, ProgressBar2, label1, label2):
        x = 0
        y = 0

        # Create Hanning window function
        window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, GuitarTuner.t.Samples_per_FFT, False)))

        # As long as we are getting data:
        while GuitarTuner.stream.is_active():
            await asyncio.sleep(delay)
            
            # Shift the buffer down and new data in
            GuitarTuner.t.get_buffer()[:-GuitarTuner.t.Frame_Size] = GuitarTuner.t.get_buffer()[GuitarTuner.t.Frame_Size:]
            GuitarTuner.t.get_buffer()[-GuitarTuner.t.Frame_Size:] = np.fromstring(GuitarTuner.stream.read(GuitarTuner.t.Frame_Size), np.int16)

            # Run the FFT on the windowed buffer
            fft = np.fft.rfft(GuitarTuner.t.get_buffer() * window)

            # Get frequency of maximum response in range
            freq = (np.abs(fft[GuitarTuner.t.get_imin():GuitarTuner.t.get_imax()]).argmax() + GuitarTuner.t.get_imin()) * GuitarTuner.t.FREQ_STEP

            # Get note number and nearest note
            n = GuitarTuner.t.freq_to_midi(freq)
            n0 = int(round(n))

            # Console output once we have a full buffer
            GuitarTuner.t.num_frames += 1

            if GuitarTuner.t.num_frames >= GuitarTuner.t.Frames_per_FFT:
                print('freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(
                    freq, GuitarTuner.t.note_name(n0), n-n0))

            
            ProgressBar1.setValue(x)
            ProgressBar2.setValue(x)
            label1.setText(str(y))
            label2.setText(str(y)+" Hz")
            x += 1
            y += 1
            if x > 98:
                x = 0
        
        else:
            await asyncio.sleep(delay)
            x = 0
            y = 0
            ProgressBar1.setValue(x)
            ProgressBar2.setValue(x)
            label1.setText(str(y))
            label2.setText(str(y)+" Hz")

        def stopper(loop):
            loop.stop()


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
    
    # hijack event loop and have control over it
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    # class instance created
    windowx = GuitarTuner()
    windowx.exec()

    with loop:
        loop.run_forever()
        loop.close()
    

    # Print initial text
    print('sampling at', windowx.t.Sampling_Freq, 'Hz with max resolution of', t.FREQ_STEP, 'Hz')
    

    sys.exit(app.exec_())
