import sys, time
import asyncio
from PyQt5.QtWidgets import QDialog, QApplication
from quamash import QEventLoop
from GUI import *
# from z import *


class MyForm(QDialog):
    def __init__(self):
        super().__init__()
        self.syncStatus = False
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.startBtn_3.clicked.connect(self.invokeAsync)
        self.ui.stopBtn_3.clicked.connect(self.pauseAsync)
        self.show()

    def invokeAsync(self):
        MyForm.syncStatus = True
        asyncio.ensure_future(self.updt(0.0001, self.ui.levelLeft_Progress_3, self.ui.levelRight_Progress_3, self.ui.curentKeyLabel_3, self.ui.frequencyLabel_3))

    def pauseAsync(self):
        MyForm.syncStatus = False

    @staticmethod
    async def updt(delay, ProgressBar1, ProgressBar2, label1, label2):
        x = 0
        y = 0
        MyForm.syncStatus = True
        #for i in range(10001):
        while True:
            if MyForm.syncStatus:
                await asyncio.sleep(delay)
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    w = MyForm()
    w.exec()
    with loop:
        loop.run_forever()
        loop.close()
    sys.exit(app.exec_())