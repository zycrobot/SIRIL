#! /home/microlab/anaconda3/envs/rosconda/bin/python

# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import cv2
print(cv2.__version__)
import bgimaging
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import numpy as np
import bgimaging
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QDesktopWidget, QCheckBox, QMessageBox
import cv2
from PyQt5.QtGui  import qRed,qGreen,qBlue





# class Getimg(QWidget):
#     eventImage = pyqtSignal()
#     def __init__(self):
#         super(Getimg,self).__init__()
#         self.hcam = None
#         self.buf = None      # video buffer
#         self.w = 0           # video width
#         self.h = 0           # video height
#         self.setFixedSize(1024, 600)
#         self.cb = QCheckBox('Auto Exposure', self)
#         self.cb.stateChanged.connect(self.changeAutoExposure)
#         try:
#             self.initCamera()
#             print("init camera!")
#         except:
#             print("camera down!!")

# # the vast majority of callbacks come from bgimaging.dll/so/dylib internal threads, 
# # so we use qt signal to post this event to the UI thread  
#     @staticmethod
#     def cameraCallback(nEvent, ctx):
#         if nEvent == bgimaging.BGIMAGING_EVENT_IMAGE:
#             ctx.eventImage.emit()

# # run in the UI thread
#     @pyqtSlot()
#     def eventImageSignal(self):
#         if self.hcam is not None:
#             try:
#                 self.hcam.PullImageV2(self.buf, 24, None)
#             except bgimaging.HRESULTException:
#                 QMessageBox.warning(self, '', 'pull image failed', QMessageBox.Ok)

#     def generatecvimg(self):
#         img = QImage(self.buf, self.w, self.h, (self.w * 24 + 31) // 32 * 4, QImage.Format_RGB888)
#         qpixmap=QPixmap.fromImage(img)
#         qimg = qpixmap.toImage()
#         temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
#         temp_shape += (4,)
#         ptr = qimg.bits()
#         ptr.setsize(qimg.byteCount())
#         result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
#         result = result[..., :3]
#         return result

#     def initCamera(self):
#         print('start open camera!')
#         a = bgimaging.Bgcam.EnumV2()
#         print("get camera name")
#         if len(a) <= 0:
#             print('No camera found')
#             self.cb.setEnabled(False)
#         else:
#             self.camname = a[0].displayname
#             self.setWindowTitle(self.camname)
#             self.eventImage.connect(self.eventImageSignal)
#             try:
#                 self.hcam = bgimaging.Bgcam.Open(a[0].id)

#                 print("open camera")
#             except bgimaging.HRESULTException:
#                 QMessageBox.warning(self, '', 'failed to open camera', QMessageBox.Ok)
#             else:
#                 self.w, self.h = self.hcam.get_Size()
#                 bufsize = ((self.w * 24 + 31) // 32 * 4) * self.h
#                 self.buf = bytes(bufsize)
#                 self.cb.setChecked(self.hcam.get_AutoExpoEnable())            
#                 try:
#                     if sys.platform == 'win32':
#                         self.hcam.put_Option(bgimaging.BGIMAGING_OPTION_BYTEORDER, 0) # QImage.Format_RGB888
                    
#                     self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
#                 except bgimaging.HRESULTException:
#                     QMessageBox.warning(self, '', 'failed to start camera', QMessageBox.Ok)

#     def changeAutoExposure(self, state):
#         if self.hcam is not None:
#             self.hcam.put_AutoExpoEnable(state == Qt.Checked)

#     def closeEvent(self, event):
#         if self.hcam is not None:
#             self.hcam.Close()
#             self.hcam = None

# class MainWin(QWidget):
#     eventImage = pyqtSignal()
    
#     def __init__(self):
#         super().__init__()
#         self.hcam = None
#         self.buf = None      # video buffer
#         self.w = 0           # video width
#         self.h = 0           # video height
#         self.total = 0
#         self.setFixedSize(1024, 600)
#         qtRectangle = self.frameGeometry()
#         centerPoint = QDesktopWidget().availableGeometry().center()
#         qtRectangle.moveCenter(centerPoint)
#         self.move(qtRectangle.topLeft())
#         self.initUI()
#         try:
#             self.initCamera()
#         except:
#             print("camera down!!")

#     def initUI(self):
#         self.cb = QCheckBox('Auto Exposure', self)
#         self.cb.stateChanged.connect(self.changeAutoExposure)
#         self.label = QLabel(self)
#         self.label.setScaledContents(True)
#         self.label.move(0, 30)
#         self.label.resize(self.geometry().width(), self.geometry().height())

# # the vast majority of callbacks come from bgimaging.dll/so/dylib internal threads, 
# # so we use qt signal to post this event to the UI thread  
#     @staticmethod
#     def cameraCallback(nEvent, ctx):
#         if nEvent == bgimaging.BGIMAGING_EVENT_IMAGE:
#             ctx.eventImage.emit()

# # run in the UI thread
#     @pyqtSlot()
#     def eventImageSignal(self):
#         if self.hcam is not None:
#             try:
#                 self.hcam.PullImageV2(self.buf, 24, None)
#                 self.total += 1
#             except bgimaging.HRESULTException:
#                 QMessageBox.warning(self, '', 'pull image failed', QMessageBox.Ok)
#             else:
#                 self.setWindowTitle('{}: {}'.format(self.camname, self.total))
                
#     def QImage2CV(self,qimg):
#         tmp = qimg
#         #using numpy 
#         print((tmp.height(), tmp.width(), 3))
#         cv_image = np.zeros((tmp.height(), tmp.width(), 3), dtype=np.uint8)
        
#         for row in range(0, tmp.height()):
#             for col in range(0,tmp.width()):
#                 print(row,col)
#                 r = qRed(tmp.pixel(col, row))
#                 g = qGreen(tmp.pixel(col, row))
#                 b = qBlue(tmp.pixel(col, row))
#                 cv_image[row,col,0] = r
#                 cv_image[row,col,1] = g
#                 cv_image[row,col,2] = b
        
#         return cv_image
    
#     def generatecvimg(self):
#         img = QImage(self.buf, self.w, self.h, (self.w * 24 + 31) // 32 * 4, QImage.Format_RGB888)
#         qpixmap=QPixmap.fromImage(img)
#         qimg = qpixmap.toImage()
#         temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
#         temp_shape += (4,)
#         ptr = qimg.bits()
#         ptr.setsize(qimg.byteCount())
#         result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
#         result = result[..., :3]
#         return result

#     def qtpixmap_to_cvimg(self,qtpixmap):
#         qimg = qtpixmap.toImage()
#         temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
#         temp_shape += (4,)
#         ptr = qimg.bits()
#         ptr.setsize(qimg.byteCount())
#         result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
#         result = result[..., :3]
#         return result

#     def initCamera(self):
#         a = bgimaging.Bgcam.EnumV2()
#         print(">>>a",len(a))
#         if len(a) <= 0:
#         # if True:
#             self.setWindowTitle('No camera found')
#             self.cb.setEnabled(False)
#         else:
#             self.camname = a[0].displayname
#             self.setWindowTitle(self.camname)
#             self.eventImage.connect(self.eventImageSignal)
#             try:
#                 self.hcam = bgimaging.Bgcam.Open(a[0].id)
#                 self.hcam.put_eSize(2)
#                 self.hcam.put_HZ(0)
#             except bgimaging.HRESULTException:
#                 QMessageBox.warning(self, '', 'failed to open camera', QMessageBox.Ok)
#             else:
#                 self.w, self.h = self.hcam.get_Size()
#                 print(">>> get resolution:",self.w, self.h)
#                 self.hz=self.hcam.get_HZ()
#                 print(">>> get Hz",self.hz)

#                 bufsize = ((self.w * 24 + 31) // 32 * 4) * self.h
#                 self.buf = bytes(bufsize)

                
#                 self.cb.setChecked(self.hcam.get_AutoExpoEnable())            
#                 try:
#                     if sys.platform == 'win32':
#                         self.hcam.put_Option(bgimaging.BGIMAGING_OPTION_BYTEORDER, 0) # QImage.Format_RGB888
#                     self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
#                 except bgimaging.HRESULTException:
#                     QMessageBox.warning(self, '', 'failed to start camera', QMessageBox.Ok)

#     def changeAutoExposure(self, state):
#         if self.hcam is not None:
#             self.hcam.put_AutoExpoEnable(state == Qt.Checked)

#     def closeEvent(self, event):
#         if self.hcam is not None:
#             self.hcam.Close()
#             self.hcam = None


class MainWin(QWidget):
    eventImage = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.hcam = None
        self.buf = None      # video buffer
        self.w = 0           # video width
        self.h = 0           # video height
        self.total = 0
        self.setFixedSize(1024, 600)
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        self.initUI()
        try:
            self.initCamera()
        except:
            print("camera down!!")

    def initUI(self):
        self.cb = QCheckBox('Auto Exposure', self)
        self.cb.stateChanged.connect(self.changeAutoExposure)
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.label.move(0, 30)
        self.label.resize(self.geometry().width(), self.geometry().height())

# the vast majority of callbacks come from bgimaging.dll/so/dylib internal threads, 
# so we use qt signal to post this event to the UI thread  
    @staticmethod
    def cameraCallback(nEvent, ctx):
        if nEvent == bgimaging.BGIMAGING_EVENT_IMAGE:
            ctx.eventImage.emit()

# run in the UI thread
    @pyqtSlot()
    def eventImageSignal(self):
        if self.hcam is not None:
            try:
                self.hcam.PullImageV2(self.buf, 24, None)
                self.total += 1
            except bgimaging.HRESULTException:
                QMessageBox.warning(self, '', 'pull image failed', QMessageBox.Ok)
            else:
                self.setWindowTitle('{}: {}'.format(self.camname, self.total))
                
    
    def generatecvimg(self):
        img = QImage(self.buf, self.w, self.h, (self.w * 24 + 31) // 32 * 4, QImage.Format_RGB888)
        qpixmap=QPixmap.fromImage(img)
        qimg = qpixmap.toImage()
        temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
        temp_shape += (4,)
        ptr = qimg.bits()
        ptr.setsize(qimg.byteCount())
        result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
        result = result[..., :3]
        return result
    

    def generatecvimg(self):
        # 假设self.buf已经是相机提供的原始图像数据
        # self.w和self.h分别是图像的宽度和高度
        # 假设图像格式是24位RGB，我们需要将其转换为OpenCV的格式

        # 计算图像的总字节数
        bufsize = self.w * self.h * 3  # RGB格式，每个像素3个字节

        # 将原始字节数据转换为NumPy数组
        # dtype=np.uint8表示每个像素值是一个无符号的8位整数
        # -1表示自动计算数组的维度
        result = np.frombuffer(self.buf, dtype=np.uint8).reshape((self.h, self.w, 3))

        # 返回OpenCV格式的图像
        return result



    def initCamera(self):
        a = bgimaging.Bgcam.EnumV2()
        print(">>>a",len(a))
        if len(a) <= 0:
        # if True:
            self.setWindowTitle('No camera found')
            self.cb.setEnabled(False)
        else:
            self.camname = a[0].displayname
            self.setWindowTitle(self.camname)
            self.eventImage.connect(self.eventImageSignal)
            try:
                self.hcam = bgimaging.Bgcam.Open(a[0].id)
                self.hcam.put_eSize(2)
                self.hcam.put_HZ(0)
            except bgimaging.HRESULTException:
                QMessageBox.warning(self, '', 'failed to open camera', QMessageBox.Ok)
            else:
                self.w, self.h = self.hcam.get_Size()
                print(">>> get resolution:",self.w, self.h)
                self.hz=self.hcam.get_HZ()
                print(">>> get Hz",self.hz)

                bufsize = ((self.w * 24 + 31) // 32 * 4) * self.h
                self.buf = bytes(bufsize)

                
                self.cb.setChecked(self.hcam.get_AutoExpoEnable())            
                try:
                    if sys.platform == 'win32':
                        self.hcam.put_Option(bgimaging.BGIMAGING_OPTION_BYTEORDER, 0) # QImage.Format_RGB888
                    self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
                except bgimaging.HRESULTException:
                    QMessageBox.warning(self, '', 'failed to start camera', QMessageBox.Ok)

    def changeAutoExposure(self, state):
        if self.hcam is not None:
            self.hcam.put_AutoExpoEnable(state == Qt.Checked)

    def closeEvent(self, event):
        if self.hcam is not None:
            self.hcam.Close()
            self.hcam = None


def main():
    # def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    #     if event == cv2.EVENT_LBUTTONDOWN:
    #         xy = "%d,%d" % (x, y)
    #         # print(x,y)
    #         # print(frame.shape)
    #         cv2.circle(frame, (x, y), 5, (255, 0, 0), thickness = 5)
    #         cv2.putText(frame, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,5.0, (0,0,0), thickness = 5)
    #         cv2.imshow("Image", frame)
    cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
    # cv2.namedWindow("Image")
    # cv2.setMouseCallback("Image", on_EVENT_LBUTTONDOWN)

    app = QApplication(sys.argv)
    win = MainWin()
    while(True):
        frame=win.generatecvimg()
        frame = cv2.pyrDown(frame)
        # frame = cv2.pyrDown(frame)
        # frame = cv2.pyrDown(frame)
        # print(frame.shape)
        frame1 = frame.copy()
        cv2.imshow('Image', frame1)
        #Waits for a user input to quit the application    
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            # del win   
            break
    cv2.destroyAllWindows()
# main()


