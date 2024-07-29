### ! /home/microlab/anaconda3/envs/rosconda/bin/python

from pickle import GLOBAL
import numpy as np
import rospy
from std_msgs.msg import String
from robot_arm_control import RobotSDK
from transformations import affine_matrix_from_points
import matplotlib.pyplot as plt
import math
import time


if __name__ == "__main__":

    arm=RobotSDK()
    arm.swichToRemoteControl()
    x0,y0,z0=arm.positionQueryInMicrometers() #current coordinate
    x_,y_,z_=x0,y0,z0
    DELTA=50

    # rbtraj=[[x0,y0,z0]]
    # for i in range(10):
    #     arm.gotoPositionInmicrometers(x0+DELTA,y0,z0)
    #     x0,y0,z0=arm.positionQueryInMicrometers()
    #     rbtraj.append([x0,y0,z0])
    #     rospy.sleep(1)
    # for i in range(10):
    #     arm.gotoPositionInmicrometers(x0,y0-DELTA,z0)
    #     x0,y0,z0=arm.positionQueryInMicrometers()
    #     rbtraj.append([x0,y0,z0])
    #     rospy.sleep(1)
    # for i in range(10):
    #     arm.gotoPositionInmicrometers(x0-DELTA,y0,z0)
    #     x0,y0,z0=arm.positionQueryInMicrometers()
    #     rbtraj.append([x0,y0,z0])
    #     rospy.sleep(1)
    # for i in range(10):
    #     arm.gotoPositionInmicrometers(x0,y0+DELTA,z0)
    #     x0,y0,z0=arm.positionQueryInMicrometers()
    #     rbtraj.append([x0,y0,z0])
    #     rospy.sleep(1)
    
    # print(*rbtraj,sep='\n')

    # arm.gotoPositionInmicrometers(x0,y0-300,z0)


    w = 40  # 圆平均分为10份
    m = (2*math.pi)/w #一个圆分成10份，每一份弧度为 m
    r = 300  #半径
    point_list = []
    for j in range(0, w):
        x = x0+r*math.sin(m*j)
        y = y0+r*math.cos(m*j)
        point_list.append([int(x),int(y)])

    arm.gotoPositionInmicrometers(point_list[0][0],point_list[0][1],z0)
    x0,y0,z0=arm.positionQueryInMicrometers()
    rbtraj=[[x0,y0,z0]]
    rospy.sleep(1)
    
    for i in range(1, w):
        arm.gotoPositionInmicrometers(point_list[i][0],point_list[i][1],z0)
        x0,y0,z0=arm.positionQueryInMicrometers()
        rbtraj.append([x0,y0,z0])
        rospy.sleep(1)
    
    arm.gotoPositionInmicrometers(x_,y_,z_)

    print(*rbtraj,sep='\n')