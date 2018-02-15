# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'password.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
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
    def setupUi(self, name):
        self.setObjectName(_fromUtf8("Wifi_Dialog"))
        self.resize(551, 39)
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setMaximumSize(QtCore.QSize(1000, 1000))
        self.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

        self.connect_btn = QtGui.QPushButton(self)
        self.connect_btn.setGeometry(QtCore.QRect(460, 7, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.connect_btn.setFont(font)
        self.connect_btn.setObjectName(_fromUtf8("connect_btn"))
        self.connect_btn.clicked.connect(self.connect_btn_clicked)

        self.name_label = QtGui.QLabel(self)
        self.name_label.setGeometry(QtCore.QRect(11, 10, 51, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.name_label.setFont(font)
        self.name_label.setObjectName(_fromUtf8("name_label"))

        self.password_lable = QtGui.QLabel(self)
        self.password_lable.setGeometry(QtCore.QRect(210, 10, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.password_lable.setFont(font)
        self.password_lable.setObjectName(_fromUtf8("password_label"))

        self.name_view = QtGui.QLabel(self)
        self.name_view.setGeometry(QtCore.QRect(60, 10, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.name_view.setFont(font)
        self.name_view.setText(_fromUtf8(""))
        self.name_view.setObjectName(_fromUtf8("name_view"))

        self.password_view = QtGui.QLineEdit(self)
        self.password_view.setGeometry(QtCore.QRect(290, 9, 151, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.password_view.setFont(font)
        self.password_view.setEchoMode(QtGui.QLineEdit.Password)
        self.password_view.setObjectName(_fromUtf8("password_view"))

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.name_view.setText(name)
        self.exec_()

    def retranslateUi(self, Wifi_Dialog):
        Wifi_Dialog.setWindowTitle(_translate("Wifi_Dialog", "Wifi Config", None))
        self.connect_btn.setText(_translate("Wifi_Dialog", "Connect", None))
        self.name_label.setText(_translate("Wifi_Dialog", "Name :", None))
        self.password_lable.setText(_translate("Wifi_Dialog", "Password", None))

    def connect_btn_clicked(self):
        ssid = self.name_view.text()
        password = self.password_view.text()

        if ssid == "":
            QtGui.QMessageBox.about(self, "Connection Error", "Please Select Wifi.")
            return

        if password == "":
            QtGui.QMessageBox.about(self, "Connection Error", "Please Input Password.")
            return

        try:
            result = Connect(ssid, password)
            if result == False:
                QtGui.QMessageBox.about(self, "Connection Error", "Oops! It looks like you may have forgotten your password.")
            else:
                self.hide()
        except:
            #QtGui.QMessageBox.about(self, "Connection Error", "Cannot Access WIFI.")
            self.hide()


