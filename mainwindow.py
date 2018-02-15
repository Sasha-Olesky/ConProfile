# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from FaceDetect import *
from WifiConfig import *
import subprocess
from subprocess import Popen, STDOUT, PIPE
from time import sleep
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

class Ui_MainWindow(object):
    process_thread = FaceDetectThread("")
    bShowProcBtns = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("ConProfile"))
        MainWindow.resize(1080, 500)
        MainWindow.setMaximumSize(1080, 500)
        MainWindow.setMinimumSize(1080, 500)
        MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.camera_view = QtGui.QLabel(self.centralwidget)
        self.camera_view.setGeometry(QtCore.QRect(10, 10, 640, 480))
        self.camera_view.setFrameShape(QtGui.QFrame.Box)
        self.camera_view.setText(_fromUtf8(""))
        self.camera_view.setObjectName(_fromUtf8("camera_view"))

        self.search_widget = QtGui.QListWidget(self.centralwidget)
        self.search_widget.setGeometry(QtCore.QRect(660, 269, 411, 221))
        self.search_widget.setObjectName(_fromUtf8("search_widget"))

        self.shot_widget = QtGui.QListWidget(self.centralwidget)
        self.shot_widget.setGeometry(QtCore.QRect(660, 40, 411, 221))
        self.shot_widget.setObjectName(_fromUtf8("shot_widget"))
        self.shot_widget.setViewMode(QtGui.QListWidget.IconMode)

        self.sorttype_combo = QtGui.QComboBox(self.centralwidget)
        self.sorttype_combo.setGeometry(QtCore.QRect(980, 10, 90, 22))
        self.sorttype_combo.setObjectName(_fromUtf8("sorttype_combo"))
        self.sorttype_combo.addItem(_fromUtf8(""))

        self.date_spin = QtGui.QDateEdit(self.centralwidget)
        self.date_spin.setGeometry(QtCore.QRect(880, 10, 90, 22))
        self.date_spin.setDateTime(QtCore.QDateTime.currentDateTime())
        self.date_spin.setDisplayFormat(('yyyy-MM-dd'))
        self.date_spin.setCalendarPopup(True)
        self.date_spin.setObjectName(_fromUtf8("date_spin"))

        self.faceshot_lbl = QtGui.QLabel(self.centralwidget)
        self.faceshot_lbl.setGeometry(QtCore.QRect(660, 5, 211, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.faceshot_lbl.setFont(font)
        self.faceshot_lbl.setObjectName(_fromUtf8("faceshot_lbl"))

        self.setting_btn = QtGui.QPushButton(self.centralwidget)
        self.setting_btn.setGeometry(QtCore.QRect(600, 442, 40, 40))
        self.setting_btn.setText(_fromUtf8(""))
        self.setting_btn.setObjectName(_fromUtf8("setting_btn"))
        self.setting_btn.setIcon(QtGui.QIcon('setting.png'))
        self.setting_btn.clicked.connect(self.on_setting_btn_clicked)

        self.start_btn = QtGui.QPushButton(self.centralwidget)
        self.start_btn.setGeometry(QtCore.QRect(490, 320, 100, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.start_btn.setFont(font)
        self.start_btn.setObjectName(_fromUtf8("start_btn"))
        self.start_btn.clicked.connect(self.on_start_btn_clicked)
        self.start_btn.hide()

        self.stop_btn = QtGui.QPushButton(self.centralwidget)
        self.stop_btn.setGeometry(QtCore.QRect(490, 350, 100, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.stop_btn.setFont(font)
        self.stop_btn.setObjectName(_fromUtf8("stop_btn"))
        self.stop_btn.clicked.connect(self.on_stop_btn_clicked)
        self.stop_btn.hide()

        self.wifi_combo = QtGui.QComboBox(self.centralwidget)
        self.wifi_combo.setGeometry(QtCore.QRect(490, 380, 100, 25))
        self.wifi_combo.setObjectName(_fromUtf8("wifi_combo"))
        self.wifi_combo.activated.connect(self.on_wifi_combo_selector)
        self.wifi_combo.hide()

        self.site_combo = QtGui.QComboBox(self.centralwidget)
        self.site_combo.setGeometry(QtCore.QRect(490, 410, 100, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.site_combo.setFont(font)
        self.site_combo.setObjectName(_fromUtf8("site_combo"))
        self.site_combo.addItem(_fromUtf8(""))
        self.site_combo.addItem(_fromUtf8(""))
        self.site_combo.addItem(_fromUtf8(""))
        self.site_combo.addItem(_fromUtf8(""))
        self.site_combo.addItem(_fromUtf8(""))
        self.site_combo.addItem(_fromUtf8(""))
        self.site_combo.hide()

        self.swap_view = QtGui.QLabel(self.centralwidget)
        self.swap_view.setGeometry(QtCore.QRect(570, 20, 60, 80))
        self.swap_view.setText(_fromUtf8(""))
        self.swap_view.setObjectName(_fromUtf8("swap_view"))

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.search_wifi()

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "ConProfile", None))
        self.sorttype_combo.setItemText(0, _translate("MainWindow", "Sort By Date", None))
        self.faceshot_lbl.setText(_translate("MainWindow", "Best Mugshots", None))
        self.start_btn.setText(_translate("MainWindow", "Start Camera", None))
        self.stop_btn.setText(_translate("MainWindow", "Stop Camera", None))
        self.site_combo.setItemText(0, _translate("MainWindow", "Google", None))
        self.site_combo.setItemText(1, _translate("MainWindow", "Bing", None))
        self.site_combo.setItemText(2, _translate("MainWindow", "Yahoo", None))
        self.site_combo.setItemText(3, _translate("MainWindow", "Baidu", None))
        self.site_combo.setItemText(4, _translate("MainWindow", "DuckDuckGo", None))
        self.site_combo.setItemText(5, _translate("MainWindow", "Yandex", None))

    def on_setting_btn_clicked(self):
        if self.bShowProcBtns:
            self.start_btn.hide()
            self.stop_btn.hide()
            self.wifi_combo.hide()
            self.site_combo.hide()
            self.bShowProcBtns = False
        else:
            self.start_btn.show()
            self.stop_btn.show()
            self.wifi_combo.show()
            self.site_combo.show()
            self.bShowProcBtns = True

    def on_start_btn_clicked(self):
        dataPath = self.show_swap_data()
        if dataPath == 'NonExist':
            print("Swap Data Error!\n")
            return
        else:
            ui.process_thread.swapPath = dataPath

        ui.process_thread.bThreading = True
        ui.process_thread.searchPath = str(self.site_combo.currentText())
        connectToMysql()

        self.process_thread.connect(self.process_thread, SIGNAL("camera(PyQt_PyObject)"), self.show_camera_data)
        self.process_thread.connect(self.process_thread, SIGNAL("face(PyQt_PyObject)"), self.show_face_data)
        self.process_thread.connect(self.process_thread, SIGNAL("search_result(PyQt_PyObject)"), self.show_search_data)
        self.process_thread.connect(self.process_thread, SIGNAL("finish(PyQt_PyObject)"), self.exit_thread)
        self.process_thread.start()

        self.start_btn.setDisabled(True)
        self.wifi_combo.setDisabled(True)
        self.site_combo.setDisabled(True)
        self.start_btn.hide()
        self.stop_btn.hide()
        self.wifi_combo.hide()
        self.site_combo.hide()
        self.bShowProcBtns = False

    def on_stop_btn_clicked(self):
        self.process_thread.bThreading = False
        self.start_btn.hide()
        self.stop_btn.hide()
        self.wifi_combo.hide()
        self.site_combo.hide()
        self.bShowProcBtns = False

    def on_wifi_combo_selector(self):
        name = str(self.wifi_combo.currentText())
        result = Ui_Wifi_Dialog()
        result.setupUi(name)

    def show_swap_data(self):
        options = QtGui.QFileDialog.Options()
        options |= QtGui.QFileDialog.DontUseNativeDialog
        caption = 'Swap Face File'
        directory = ''
        filter = 'Image Files (*.jpg);;Image Files (*.png)'
        fileName = QtGui.QFileDialog.getOpenFileName(None, caption, directory, filter, options=options)
        swapData = cv2.imread(str(fileName))
        display = cv2.cvtColor(swapData, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(display, display.shape[1], display.shape[0], display.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)

        pix = QtGui.QPixmap(image)
        self.swap_view.setPixmap(pix)
        self.swap_view.setScaledContents(True)

        gray = cv2.cvtColor(swapData, cv2.COLOR_BGR2GRAY)
        detector = dlib.get_frontal_face_detector()
        dets = detector(gray, 1)
        bExistFace = False
        for i, d in enumerate(dets):
            bExistFace = True
            break

        if bExistFace:
            return str(fileName);
        else:
            return 'NonExist'

    def show_camera_data(self, frame):
        display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(display, display.shape[1], display.shape[0], display.shape[1] * 3,
                             QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image)
        self.camera_view.setPixmap(pix)
        self.camera_view.setScaledContents(True)

    def show_face_data(self, faces):
        for i, face in enumerate(faces):
            self.shot_widget.clear()

        for i, face in enumerate(faces):
            item = QtGui.QListWidgetItem()
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(_fromUtf8(face)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            item.setIcon(icon)
            self.shot_widget.addItem(item)

    def show_search_data(self, result):
        item = QtGui.QListWidgetItem(result)
        self.search_widget.addItem(item)

    def search_wifi(self):
        #cells = Search()
        #for cell in cells:
        #    if cell.ssid == "":
        #        self.wifi_combo.addItem(cell.ssid)

        wifi_list = subprocess.check_output(["netsh", "wlan", "show", "network"])
        results = wifi_list.decode("ascii")  # needed in python 3
        results = results.replace("\r", "")
        ls = results.split("\n")
        ls = ls[4:]
        ssids = []
        x = 0
        while x < len(ls):
            if x % 5 == 0:
                ssid = ls[x][9:]
                ssids.append(ssid)
            x += 1

        for i, ssid in enumerate(ssids):
            if ssid != "":
                self.wifi_combo.addItem(ssid)

    def exit_thread(self, bExit):
        self.start_btn.setDisabled(False)
        self.wifi_combo.setDisabled(False)
        self.site_combo.setDisabled(False)
        self.camera_view.clear()
        self.shot_widget.clear()
        self.swap_view.clear()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    ui.process_thread.bThreading = False
    sys.exit()

