# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'WifiDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Wifi_Dialog(object):
    def setupUi(self, Wifi_Dialog):
        Wifi_Dialog.setObjectName(_fromUtf8("Wifi_Dialog"))
        Wifi_Dialog.resize(480, 242)
        Wifi_Dialog.setMinimumSize(QtCore.QSize(0, 0))
        Wifi_Dialog.setMaximumSize(QtCore.QSize(1000, 1000))
        Wifi_Dialog.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

        self.wifi_list = QtGui.QListView(Wifi_Dialog)
        self.wifi_list.setGeometry(QtCore.QRect(10, 10, 461, 191))
        self.wifi_list.setObjectName(_fromUtf8("wifi_list"))

        self.connect_btn = QtGui.QPushButton(Wifi_Dialog)
        self.connect_btn.setGeometry(QtCore.QRect(397, 212, 75, 23))
        self.connect_btn.setObjectName(_fromUtf8("connect_btn"))

        self.name_label = QtGui.QLabel(Wifi_Dialog)
        self.name_label.setGeometry(QtCore.QRect(16, 215, 41, 16))
        self.name_label.setObjectName(_fromUtf8("name_label"))
        self.password_lable = QtGui.QLabel(Wifi_Dialog)
        self.password_lable.setGeometry(QtCore.QRect(170, 215, 51, 16))
        self.password_lable.setObjectName(_fromUtf8("password_lable"))

        self.name_view = QtGui.QLabel(Wifi_Dialog)
        self.name_view.setGeometry(QtCore.QRect(60, 215, 101, 16))
        self.name_view.setText(_fromUtf8(""))
        self.name_view.setObjectName(_fromUtf8("name_view"))

        self.password_view = QtGui.QLineEdit(Wifi_Dialog)
        self.password_view.setGeometry(QtCore.QRect(230, 214, 151, 20))
        self.password_view.setObjectName(_fromUtf8("password_view"))

        self.retranslateUi(Wifi_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Wifi_Dialog)

    def retranslateUi(self, Wifi_Dialog):
        Wifi_Dialog.setWindowTitle(_translate("Wifi_Dialog", "Face Recognition", None))
        self.connect_btn.setText(_translate("Wifi_Dialog", "Connect", None))
        self.name_label.setText(_translate("Wifi_Dialog", "Name :", None))
        self.password_lable.setText(_translate("Wifi_Dialog", "Password", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Wifi_Dialog = QtGui.QDialog()
    ui = Ui_Wifi_Dialog()
    ui.setupUi(Wifi_Dialog)
    Wifi_Dialog.show()
    sys.exit(app.exec_())

