# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WifiDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from WifiControl import *

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

class Ui_Wifi_Dialog(QtGui.QDialog):
    def setupUi(self):
        self.setObjectName(_fromUtf8("Wifi_Dialog"))
        self.resize(480, 242)
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setMaximumSize(QtCore.QSize(1000, 1000))
        self.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

        self.wifi_list = QtGui.QListWidget(self)
        self.wifi_list.setGeometry(QtCore.QRect(10, 10, 461, 191))
        self.wifi_list.setObjectName(_fromUtf8("wifi_list"))
        self.wifi_list.clicked.connect(self.get_data)

        self.connect_btn = QtGui.QPushButton(self)
        self.connect_btn.setGeometry(QtCore.QRect(397, 212, 75, 23))
        self.connect_btn.setObjectName(_fromUtf8("connect_btn"))
        self.connect_btn.clicked.connect(self.connect_wifi)

        self.name_label = QtGui.QLabel(self)
        self.name_label.setGeometry(QtCore.QRect(16, 215, 41, 16))
        self.name_label.setObjectName(_fromUtf8("name_label"))

        self.password_lable = QtGui.QLabel(self)
        self.password_lable.setGeometry(QtCore.QRect(160, 215, 61, 16))
        self.password_lable.setObjectName(_fromUtf8("password_lable"))

        self.name_view = QtGui.QLabel(self)
        self.name_view.setGeometry(QtCore.QRect(60, 215, 101, 16))
        self.name_view.setText(_fromUtf8(""))
        self.name_view.setObjectName(_fromUtf8("name_view"))

        self.password_view = QtGui.QLineEdit(self)
        self.password_view.setGeometry(QtCore.QRect(230, 214, 151, 20))
        self.password_view.setEchoMode(QLineEdit.Password)
        self.password_view.setObjectName(_fromUtf8("password_view"))

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.search_wifi()
        self.exec_()

    def connect_wifi(self):
        ssid = self.name_view.text()
        password = self.password_view.text()

        try:
            result = Connect(ssid, password)
            if result == False:
                QMessageBox.about(self, "Connection Error", "Oops! It looks like you may have forgotten your password.")
            else:
                self.hide()
        except:
            QMessageBox.about(self, "Connection Error", "Cannot Access WIFI.")
            self.hide()

    def get_data(self):
        current = self.wifi_list.selectedItems()
        for current in list(current):
            name = str(current.text())
            self.name_view.setText(name)

    def search_wifi(self):
        try:
            wifi_list = Search()
        except:
            QMessageBox.about(self, "Search Error", "Cannot Search WIFI.")
            for i in range(10):
                item = QListWidgetItem("test wifi %i" % i)
                self.wifi_list.addItem(item)

    def retranslateUi(self, Wifi_Dialog):
        Wifi_Dialog.setWindowTitle(_translate("Wifi_Dialog", "Face Recognition", None))
        self.connect_btn.setText(_translate("Wifi_Dialog", "Connect", None))
        self.name_label.setText(_translate("Wifi_Dialog", "Name :", None))
        self.password_lable.setText(_translate("Wifi_Dialog", "Password", None))


