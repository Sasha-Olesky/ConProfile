#from PyQt4.QtCore import QThread, SIGNAL
import threading, time, Queue
import numpy as np
import cv2
import dlib
from FaceSwap import *
from GoogleSearch import *

class FaceDetectThread(QThread):

    bThreading = True
    swapPath = "";
    searchPath = "";

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
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320);
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240);
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
                displayFrame = frame.copy()
                for i, d in enumerate(dets):
                    faceMaxCnt = faceMaxCnt + 1
                    exist = True

                self.swapFace(displayFrame, dets)

                if exist == True:
                    for counter in range(0, 10):
                        if self.bThreading == False:
                            break;
                        ret, procFrame = cap.read()
                        procFrame = cv2.flip(procFrame, 1)
                        tempFrame = procFrame.copy()
                        if ret == True:
                            gray = cv2.cvtColor(procFrame, cv2.COLOR_BGR2GRAY)
                            tempFaces = detector(gray, 1)
                            faceCnt = 0

                            for i, d in enumerate(tempFaces):
                                faceCnt = faceCnt + 1

                            if faceCnt >= faceMaxCnt:
                                faces = tempFaces
                                frame = procFrame

                            self.swapFace(tempFrame, tempFaces)

                    result_faces = []
                    for i, d in enumerate(faces):
                        if self.bThreading == False:
                            break;

                        height, width, channels = frame.shape

                        unit = (d.right() - d.left()) / 2

                        x1 = int(d.left() - unit * 1.5)
                        y1 = int(d.top() - unit * 1.5)
                        x2 = int(d.right() + unit * 1.5)
                        y2 = int(d.bottom() + unit * 2.5)
                        if (x1 < 0): x1 = 4
                        if (x2 >= width): x2 = width - 5
                        if (y1 < 0): y1 = 4
                        if (y2 >= height): y2 = height - 5
                        try:
                            roi_color = frame[y1:y2, x1:x2]
                        except:
                            continue

                        tempX1 = d.left()
                        tempY1 = d.top()
                        tempX2 = d.right()
                        tempY2 = d.bottom()
                        if (tempX1 < 0): tempX1 = 4
                        if (tempX2 >= width): tempX2 = width - 5
                        if (tempY1 < 0): tempY1 = 4
                        if (tempY2 >= height): tempY2 = height - 5
                        try:
                            temp_color = frame[tempY1:tempY2, tempX1:tempX2]
                        except:
                            continue

                        if faceIdx == 0:
                            name = str('faces/') + str(faceIdx) + '.png'
                            templateName = str('faceTemplates/') + str(faceIdx) + '.png'
                            result_faces.append(templateName)
                            cv2.imwrite(name, roi_color)
                            cv2.imwrite(templateName, temp_color)
                            print("New Face")
                            savefile = str(faceIdx) + '.png'
                            self.searchData(savefile)
                            faceIdx = faceIdx + 1
                        else:
                            bExistFace = False
                            existFaceIdx = -1
                            for beforeIdx in range(0, faceIdx):
                                full_path = os.getcwd()
                                full_path = full_path.replace("\\", "/")
                                filePath = full_path + "/faceTemplates/" + str(beforeIdx) + '.png'
                                orgImg = cv2.imread(filePath)

                                bExistFace = self.recogFace(orgImg, temp_color)
                                if bExistFace == True:
                                    existFaceIdx = beforeIdx
                                    break

                            if bExistFace == False:
                                name = str('faces/') + str(faceIdx) + '.png'
                                templateName = str('faceTemplates/') + str(faceIdx) + '.png'
                                result_faces.append(templateName)
                                cv2.imwrite(name, roi_color)
                                cv2.imwrite(templateName, temp_color)
                                print("New Face")
                                savefile = str(faceIdx) + '.png'
                                self.searchData(savefile)
                                faceIdx = faceIdx + 1
                            else:
                                print("Exist Face")
                                # --------- udpate people_table when face exists already. ------------
                                imagePath = str(existFaceIdx) + '.png'
                                updatePeopelTable(imagePath)

                    self.emit(SIGNAL('face(PyQt_PyObject)'), result_faces)
            else:
                print("Error Connecting Camera")
                break

        cap.release()
        self.emit(SIGNAL('finish(PyQt_PyObject)'), True)
        self.quit()

    def searchData(self, filename):
        full_path = os.getcwd()
        full_path = full_path.replace("\\", "/")
        filePath = full_path + "/faces/" + filename

        _searchTread = threading.Thread(target=searchInfo, args=(self, filePath, self.searchPath, False))
        _searchTread.start()

    def recogFace(self, orgImg, faceImg):
        try:
            orgImg = cv2.cvtColor(orgImg, cv2.COLOR_BGR2GRAY)
            faceImg = cv2.cvtColor(faceImg, cv2.COLOR_BGR2GRAY)
            w, h = orgImg.shape[::-1]
            res = cv2.matchTemplate(faceImg, orgImg, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                return True
            return False
        except:
            print("Error Template Matching")
            return False

    def swapFace(self, orgImg, faceRects):
        swapImg = cv2.imread(str(self.swapPath))

        for i, d in enumerate(faceRects):
            height, width, channels = orgImg.shape

            X1 = d.left()
            Y1 = d.top()
            X2 = d.right()
            Y2 = d.bottom()
            if (X1 < 0): X1 = 4
            if (X2 >= width): X2 = width - 5
            if (Y1 < 0): Y1 = 4
            if (Y2 >= height): Y2 = height - 5
            try:
                org = orgImg[Y1:Y2, X1:X2]
                orgImg[Y1:Y2, X1:X2] = faceSwap(org, swapImg)
                cv2.rectangle(orgImg, (d.left(), d.top()), (d.right(), d.bottom()), (0, 255, 0), 2)
            except:
                continue

        self.emit(SIGNAL('camera(PyQt_PyObject)'), orgImg)