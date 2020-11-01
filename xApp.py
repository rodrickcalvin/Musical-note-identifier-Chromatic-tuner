import sys, time, asyncio
from quamash import QEventLoop
import pyaudio
from PyQt5.QtWidgets import QDialog, QApplication
from GUI import *
from logic import *
from xAudioControl import xAudio

class GuitarTuner(QDialog):
    t = TunerLogic("Ukulele")

    # Initialize audio
    xAudio

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
        asyncio.ensure_future(
            self.updt(0.0001, self.ui.levelLeft_Progress_3, self.ui.levelRight_Progress_3, self.ui.curentKeyLabel_3,
                      self.ui.frequencyLabel_3))
        xAudio.stopStreamStatus = True;

    def pauseAsync(self):
        # GuitarTuner.syncStatus = False
        xAudio.streamStatus = False

    @staticmethod
    async def updt(delay, ProgressBar1, ProgressBar2, label1, label2):
        #xAudio.startStream()
        while True:
            await asyncio.sleep(delay)
            if (xAudio.streamStatus):
                xAudio.count += 1
                xAudio.buf[:-xAudio.FRAME_SIZE] = xAudio.buf[xAudio.FRAME_SIZE:]
                xAudio.buf[-xAudio.FRAME_SIZE:] = np.fromstring(xAudio.stream.read(xAudio.FRAME_SIZE), np.int16)
                xAudio.fft = np.fft.rfft(xAudio.buf * xAudio.window)
                xAudio.freq = (np.abs(xAudio.fft[xAudio.imin:xAudio.imax]).argmax() + xAudio.imin) * xAudio.FREQ_STEP
                xAudio.n = xAudio.freq_to_number(xAudio.freq)
                xAudio.n0 = int(round(xAudio.n))
                xAudio.num_frames += 1

                if xAudio.num_frames >= xAudio.FRAMES_PER_FFT:
                    print(str(xAudio.count)+' freq: {:7.2f} Hz     note: {:>3s} {:+.2f}'.format(xAudio.freq, xAudio.note_name(xAudio.n0), xAudio.n - xAudio.n0))
                    windowx.setKey('{:>3s}'.format(xAudio.note_name(xAudio.n0)))
                    windowx.setFrequency('({:7.2f} Hz)'.format(xAudio.freq))


        else:
            await asyncio.sleep(delay)

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

    sys.exit(app.exec_())