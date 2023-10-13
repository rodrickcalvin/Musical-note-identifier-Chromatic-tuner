import traceback, sys, time, os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from GUI import *

class Worker(QRunnable):
    @pyqtSlot()
    def __init__(self):
        super().__init__()
        from xAudioControl import xAudio
        self.xAudio = xAudio()
        self.xAudio.__init__()
    def startStream(self):
        self.xAudio.setStreamOn()
    def stopStream(self):
        self.xAudio.setStreamOff()
    def exitStream(self):
        self.xAudio.exitStream()
        QCoreApplication.quit()
        os._exit(0)

    def setNoteMinMax(self, noteMin1, noteMax1):
        self.xAudio.setNoteMinMax(noteMin1, noteMax1)
    def run(self):
        while True:
            self.xAudio.startStream()
            if (self.xAudio.streamStatus):
                windowx.setKey(self.xAudio.keyy)
                windowx.setFrequency(self.xAudio.freqy)
        time.sleep(0.005)

worker = Worker()
class GuitarTuner(QDialog):
    def __init__(self):
        super().__init__()
        self.threadpool = QThreadPool()
        self.threadpool2 = QThreadPool()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # self.ui.startBtn_3.clicked.connect(lambda: self.setLeftPercentageBar(100))
        self.ui.startBtn_3.clicked.connect(lambda: worker.startStream())
        self.ui.stopBtn_3.clicked.connect(lambda: worker.stopStream())
        self.ui.exitBtn_3.clicked.connect(lambda: worker.exitStream())
        self.ui.instrumentChooserComboxBox_3.currentIndexChanged.connect(lambda: self.setNoteMinMax(self.ui.instrumentChooserComboxBox_3.currentText()))
        self.startThread()
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

    def setNoteMinMax(self, instrumentName):
        # BASS GUITAR
        if instrumentName == "Bass Guitar":
            worker.setNoteMinMax(23, 48)
        # ACOUSTIC/ELECTRIC GUITAR
        elif instrumentName == "Acoustic/Electric Guitar":
            worker.setNoteMinMax(40, 64)
        # UKULELE
        elif instrumentName == "Ukulele":
            worker.setNoteMinMax(60, 69)
        # PIANO
        elif instrumentName == "Piano": # A0 TO C8
            worker.setNoteMinMax(21, 108)

    def startThread(self):
        self.threadpool.start(worker)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # class instance created
    windowx = GuitarTuner()
    sys.exit(app.exec_())