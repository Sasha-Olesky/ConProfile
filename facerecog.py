from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QThread, SIGNAL
import threading,time
import numpy as np
import cv2
import dlib
import os
from face_search import *

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

def searchData(filename):
    full_path = os.getcwd()
    full_path = full_path.replace("\\", "/")
    filePath = full_path + "/faces/" + filename

    _searchTread = threading.Thread(target=searchInfoFromGoogle, args=(filePath, False,))
    _searchTread.start()

def recogFace(orgImg, faceImg):
    orgImg = cv2.cvtColor(orgImg, cv2.COLOR_BGR2GRAY)
    faceImg = cv2.cvtColor(faceImg, cv2.COLOR_BGR2GRAY)
    w, h = orgImg.shape[::-1]
    res = cv2.matchTemplate(faceImg, orgImg, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        return True
    return False

class getPostThread(QThread):

    bThreading = True
    def __init__(self, path):
        QThread.__init__(self)
        self.path = path

    def __del__(self):
        self.wait()

    def setPath(self, path):
        self.path = path

    def run(self):
        if not os.path.exists('faces'):
            os.makedirs(str('faces'))

        if not os.path.exists('faceTemplates'):
            os.makedirs(str('faceTemplates'))

        faceIdx = 0
        fileList = os.listdir(str('faces'))
        for fileName in fileList:
            faceIdx = faceIdx + 1

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_AUTOFOCUS, False)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640);
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480);
        codec = 1196444237.0  # MJPG
        cap.set(cv2.CAP_PROP_FOURCC, codec)
        if (cap.isOpened() == False):
            print("Error Connecting Camera")

        detector = dlib.get_frontal_face_detector()

        while (cap.isOpened()):
            if self.bThreading == False:
                break;
            ret, frame = cap.read()
            if ret == True:
                frame = cv2.flip(frame, 1)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faceMaxCnt = 0
                exist = False

                dets = detector(gray, 1)
                for i, d in enumerate(dets):
                    faceMaxCnt = faceMaxCnt + 1
                    exist = True

                if exist == True:
                    for counter in range(0, 10):
                        if self.bThreading == False:
                            break;
                        ret, procFrame = cap.read()
                        procFrame = cv2.flip(procFrame, 1)
                        if ret == True:
                            gray = cv2.cvtColor(procFrame, cv2.COLOR_BGR2GRAY)
                            tempFaces = detector(gray, 1)
                            faceCnt = 0

                            if counter == 0:
                                faces = tempFaces
                                frame = procFrame
                            else:
                                for i, d in enumerate(tempFaces):
                                    cv2.rectangle(procFrame, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)
                                    faceCnt = faceCnt + 1

                                if faceCnt > faceMaxCnt:
                                    faces = tempFaces
                                    frame = procFrame

                            self.emit(SIGNAL('signal(PyQt_PyObject)'), procFrame)

                    for i, d in enumerate(faces):
                        if self.bThreading == False:
                            break;
                        x = d.left()
                        y = d.top()
                        w = d.right() - d.left()
                        h = d.bottom() - d.top()
                        #height, width, channels = frame.shape
                        #x1 = x - w / 2
                        #x2 = x + w  + w / 2
                        #y1 = y - h / 2
                        #y2 = y + h + w / 2
                        #if x1 < 0:
                        #    x1 = 1
                        #if y1 < 0:
                        #    y1 = 1
                        #if x2 > width - 2:
                        #    x2 = width - 2
                        #if y2 > height -2:
                        #    y2 = height -2

                        roi_color = frame[y:y+h, x:x+w]
                        temp_color = frame[y:y+h, x:x+w]
                        if faceIdx == 0:
                            name = str('faces/') + str(faceIdx) + '.png'
                            templateName = str('faceTemplates/') + str(faceIdx) + '.png'
                            cv2.imwrite(name, roi_color)
                            cv2.imwrite(templateName, temp_color)
                            print("New Face")
                            savefile = str(faceIdx) + '.png'
                            searchData(savefile)
                            faceIdx = faceIdx + 1
                        else:
                            bExistFace = False
                            existFaceIdx = -1
                            for beforeIdx in range(0, faceIdx):
                                full_path = os.getcwd()
                                full_path = full_path.replace("\\", "/")
                                filePath = full_path + "/faceTemplates/" + str(beforeIdx) + '.png'
                                orgImg = cv2.imread(filePath)
                                bExistFace = recogFace(orgImg, temp_color)
                                if bExistFace == True:
                                    existFaceIdx = beforeIdx
                                    break

                            if bExistFace == False:
                                name = str('faces/') + str(faceIdx) + '.png'
                                templateName = str('faceTemplates/') + str(faceIdx) + '.png'
                                cv2.imwrite(name, roi_color)
                                cv2.imwrite(templateName, temp_color)
                                print("New Face")
                                savefile = str(faceIdx) + '.png'
                                searchData(savefile)
                                faceIdx = faceIdx + 1
                            else:
                                print("Exist Face")
                                # --------- udpate people_table when face exists already. ------------
                                imagePath = str(existFaceIdx) + '.png'
                                updatePeopelTable(imagePath)
                else:
                    self.emit(SIGNAL('signal(PyQt_PyObject)'), frame)
            else:
                print("Error Connecting Camera")
                break

        cap.release()
        self.quit()

class Ui_Dialog(object):
    get_thread = getPostThread("")

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(640, 520)
        Dialog.setMinimumSize(QtCore.QSize(640, 520))
        Dialog.setMaximumSize(QtCore.QSize(640, 520))
        Dialog.setWindowFlags(QtCore.Qt.WindowMaximizeButtonHint)

        self.camera_view = QtGui.QLabel(Dialog)
        self.camera_view.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.camera_view.setMinimumSize(QtCore.QSize(640, 480))
        self.camera_view.setMaximumSize(QtCore.QSize(640, 480))
        self.camera_view.setFrameShape(QtGui.QFrame.Box)
        self.camera_view.setFrameShadow(QtGui.QFrame.Plain)
        self.camera_view.setText(_fromUtf8(""))
        self.camera_view.setObjectName(_fromUtf8("camera_view"))
        self.start_btn = QtGui.QPushButton(Dialog)
        self.start_btn.setGeometry(QtCore.QRect(280, 490, 75, 23))
        self.start_btn.setObjectName(_fromUtf8("start_btn"))
        self.start_btn.clicked.connect(self.start)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Face Recognition", None))
        self.start_btn.setText(_translate("Dialog", "Start", None))

    def start(self):
        connectToMysql()
        self.get_thread.connect(self.get_thread, SIGNAL("signal(PyQt_PyObject)"), self.setPixmap)
        self.get_thread.start()
        self.start_btn.setDisabled(True)

    def stop(self):
        self.get_thread.terminate()
        self.get_thread.killTimer(1)

    def setPixmap(self, frame):
        display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = QtGui.QImage(display, display.shape[1], display.shape[0], display.shape[1] * 3, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap(image)
        self.camera_view.setPixmap(pix)
        self.camera_view.setScaledContents(True)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec_()
    ui.get_thread.bThreading = False
    sys.exit()