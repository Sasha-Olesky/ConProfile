# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FaceDetect import *
from WifiControl import *
from WifiDialog import *
import cv2

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class WiFiDialog(QtGui.QDialog):
  def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Wifi_Dialog()
        self.ui.setupUi(self)

class Ui_Main_Window(object):
    process_thread = getPostThread("")

    def setupUi(self, Main_Window):
        Main_Window.setObjectName(_fromUtf8("Main_Window"))
        Main_Window.resize(480, 601)
        Main_Window.setMinimumSize(QtCore.QSize(0, 0))
        Main_Window.setMaximumSize(QtCore.QSize(1000, 1000))
        Main_Window.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

        self.process_group = QtGui.QGroupBox(Main_Window)
        self.process_group.setGeometry(QtCore.QRect(10, 10, 461, 391))
        self.process_group.setObjectName(_fromUtf8("process_group"))

        self.camera_view = QtGui.QLabel(self.process_group)
        self.camera_view.setGeometry(QtCore.QRect(10, 50, 441, 331))
        self.camera_view.setMinimumSize(QtCore.QSize(0, 0))
        self.camera_view.setMaximumSize(QtCore.QSize(640, 480))
        self.camera_view.setFrameShape(QtGui.QFrame.Box)
        self.camera_view.setFrameShadow(QtGui.QFrame.Plain)
        self.camera_view.setText(_fromUtf8(""))
        self.camera_view.setObjectName(_fromUtf8("camera_view"))

        self.wifi_connect_btn = QtGui.QPushButton(self.process_group)
        self.wifi_connect_btn.setGeometry(QtCore.QRect(240, 20, 101, 23))
        self.wifi_connect_btn.setObjectName(_fromUtf8("wifi_connect_btn"))
        self.wifi_connect_btn.clicked.connect(self.connect_wifi)

        self.camera_connect_btn = QtGui.QPushButton(self.process_group)
        self.camera_connect_btn.setGeometry(QtCore.QRect(350, 20, 101, 23))
        self.camera_connect_btn.setObjectName(_fromUtf8("camera_connect_btn"))
        self.camera_connect_btn.clicked.connect(self.connect_camera)

        self.result_group = QtGui.QGroupBox(Main_Window)
        self.result_group.setGeometry(QtCore.QRect(10, 410, 461, 161))
        self.result_group.setObjectName(_fromUtf8("result_group"))

        self.face_view = QtGui.QLabel(self.result_group)
        self.face_view.setGeometry(QtCore.QRect(320, 20, 131, 131))
        self.face_view.setMinimumSize(QtCore.QSize(0, 0))
        self.face_view.setMaximumSize(QtCore.QSize(640, 480))
        self.face_view.setFrameShape(QtGui.QFrame.Box)
        self.face_view.setFrameShadow(QtGui.QFrame.Plain)
        self.face_view.setText(_fromUtf8(""))
        self.face_view.setObjectName(_fromUtf8("face_view"))

        self.search_result_table = QtGui.QTableView(self.result_group)
        self.search_result_table.setGeometry(QtCore.QRect(10, 20, 301, 131))
        self.search_result_table.setObjectName(_fromUtf8("search_result_table"))

        self.retranslateUi(Main_Window)
        QtCore.QMetaObject.connectSlotsByName(Main_Window)

    def retranslateUi(self, Main_Window):
        Main_Window.setWindowTitle(_translate("Main_Window", "Face Recognition", None))
        self.process_group.setTitle(_translate("Main_Window", "Process", None))
        self.wifi_connect_btn.setText(_translate("Main_Window", "Connect Wifi", None))
        self.camera_connect_btn.setText(_translate("Main_Window", "Connect Camera", None))
        self.result_group.setTitle(_translate("Main_Window", "Result", None))

    def connect_camera(self):
        connectToMysql()
        self.process_thread.connect(self.process_thread, SIGNAL("camera(PyQt_PyObject)"), self.show_camera)
        self.process_thread.connect(self.process_thread, SIGNAL("face(PyQt_PyObject)"), self.show_face)
        self.process_thread.start()
        self.process_thread.setDisabled(True)

    def show_camera(self, frame):
        display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(display, display.shape[1], display.shape[0], display.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image)
        self.camera_view.setPixmap(pix)
        self.camera_view.setScaledContents(True)

    def show_face(self, face):
        display = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(display, display.shape[1], display.shape[0], display.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image)
        self.face_view.setPixmap(pix)
        self.face_view.setScaledContents(True)

    def connect_wifi(self):
        Dialog = WiFiDialog(self)
        Dialog.show()
        ret = Dialog.exec_()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Main_Window = QtGui.QDialog()
    ui = Ui_Main_Window()
    ui.setupUi(Main_Window)
    Main_Window.show()
    app.exec_()
    ui.process_thread.bThreading = False
    sys.exit()

