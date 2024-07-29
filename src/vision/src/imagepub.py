#! /home/microlab/anaconda3/envs/rosconda/bin/python

import sys
sys.path.append('../')
import cv2
print(cv2.__version__)

import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Image
import time
from Getimg import MainWin
from PyQt5.QtWidgets import QApplication
import numpy as np



if __name__=="__main__":
    rospy.init_node('camera_node', anonymous=True)

    topic=rospy.get_param("~topic",default='/rawimage')
    rospy.loginfo(topic)

    image_pub=rospy.Publisher(topic, Image, queue_size = 10)

    app=QApplication(sys.argv)
    win=MainWin()
  

    header = Header(stamp = rospy.Time.now())
    header.frame_id = "Camera"
    ros_frame = Image()
    ros_frame.header=header
    ros_frame.width = 912
    ros_frame.height = 608
    ros_frame.encoding = "bgr8"

    fre=0

    cv2.namedWindow("imagepub",cv2.WINDOW_NORMAL)
    while not rospy.is_shutdown():
        start = time.time()
        frame = win.generatecvimg()
        frame1 = cv2.flip(frame,0)
        frame1 = cv2.pyrDown(frame1)
        frame1 = frame1[:, :, [2, 1, 0]]
        # print(frame1.shape)


        ros_frame.data = np.array(frame1).tobytes()

        if fre%5==0:
            image_pub.publish(ros_frame) 

        
        fre+=1
        fre%=10000


        end = time.time()
        if end-start>0:
            fps=1/(end-start)
            cv2.putText(frame1, "FPS {0}".format(float('%.1f' % (fps))), (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255),3)

        rate = rospy.Rate(100)
        cv2.imshow('imagepub',frame1)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    cv2.destroyAllWindows() 
    print("quit successfully!")