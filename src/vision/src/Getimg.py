#! /home/microlab/anaconda3/envs/rosconda/bin/python

# -*- coding: utf-8 -*-
import sys
sys.path.append('../')
import cv2
print(cv2.__version__)
import bgimaging

import numpy as np
import numpy as np
import bgimaging
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import  QApplication, QWidget
import time


class MainWin(QWidget):
    eventImage = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.hcam = None
        self.buf = None      # video buffer
        self.w = 0           # video width
        self.h = 0           # video height
        self.total = 0


        self.initUI()
        try:
            self.initCamera()
        except:
            print("camera down!!")

    def initUI(self):

        pass


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
                # print('PullImageV2',self.total)
                self.total += 1
            except bgimaging.HRESULTException:
                print( 'pull image failed')
                
    

    def generatecvimg(self):
        result = np.frombuffer(self.buf, dtype=np.uint8).reshape((self.h, self.w, 3))
        return result


    def initCamera(self):
        a = bgimaging.Bgcam.EnumV2()
        print(">>>a",len(a))
        if len(a) <= 0:
        # if True:
            print('No camera found')
        else:
            self.camname = a[0].displayname

            self.eventImage.connect(self.eventImageSignal)

            self.hcam = bgimaging.Bgcam.Open(a[0].id)
            self.hcam.put_eSize(2)
            self.hcam.put_HZ(0)
            self.w, self.h = self.hcam.get_Size()
            self.hcam.put_AutoExpoEnable(1)
            # self.hcam.put_MaxAutoExpoTimeAGain(70,1)
            self.hcam.put_AutoExpoTarget(50)
            # self.hcam.put_ExpoTime(70)
            print(">>> get resolution:",self.w, self.h)
            self.hz=self.hcam.get_HZ()
            print(">>> get Hz",self.hz)
            bufsize = ((self.w * 24 + 31) // 32 * 4) * self.h
            self.buf = bytes(bufsize)
            self.hcam.StartPullModeWithCallback(self.cameraCallback, self)
            # self.hcam.put_AutoExpoEnable




    def __del__(self):
            # super().__del__()
            # 析构函数：执行清理工作
            print("MainWin is being deleted. Cleaning up resources...")

            # 关闭相机
            if self.hcam is not None:
                try:
                    # 关闭相机句柄
                    self.hcam.Close()
                    self.hcam = None
                    print("Camera resources released successfully.")
                except Exception as e:
                    print(f"Failed to release camera resources: {e}")
            


def main():
    cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
    app = QApplication(sys.argv)
    win = MainWin()
    while(True):
        start = time.time()
        frame=win.generatecvimg()
        # frame = cv2.pyrDown(frame)
        # frame = cv2.pyrDown(frame)
        # frame = cv2.pyrDown(frame)
        # print(frame.shape)
        frame1 = frame.copy()
        

        end = time.time()
        if end-start>0:
            fps=1/(end-start)
            cv2.putText(frame1, "FPS {0}".format(float('%.1f' % (fps))), (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),8)
        #Waits for a user input to quit the application    
        cv2.imshow('Image', frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            del win   
            break
    cv2.destroyAllWindows()

# main()


