# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tuner.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Window(object):
    def setupUi(self, Window):
        Window.setObjectName("Window")
        Window.resize(596, 450)
        self.sensor = QtWidgets.QSlider(Window)
        self.sensor.setGeometry(QtCore.QRect(20, 260, 551, 41))
        self.sensor.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.Uganda))
        self.sensor.setMaximum(1000)
        self.sensor.setPageStep(1)
        self.sensor.setOrientation(QtCore.Qt.Horizontal)
        self.sensor.setTickInterval(0)
        self.sensor.setObjectName("sensor")
        self.graphicsView = QtWidgets.QGraphicsView(Window)
        self.graphicsView.setGeometry(QtCore.QRect(240, 90, 111, 101))
        self.graphicsView.setObjectName("graphicsView")

        self.retranslateUi(Window)
        QtCore.QMetaObject.connectSlotsByName(Window)

    def retranslateUi(self, Window):
        _translate = QtCore.QCoreApplication.translate
        Window.setWindowTitle(_translate("Window", "Frame"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Window = QtWidgets.QFrame()
    ui = Ui_Window()
    ui.setupUi(Window)
    Window.show()
    sys.exit(app.exec_())
