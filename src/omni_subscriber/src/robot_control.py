#! /home/microlab/anaconda3/envs/rosconda/bin/python

from pickle import GLOBAL
import numpy as np
import rospy
from std_msgs.msg import String
from robot_arm_control import RobotSDK
from transformations import affine_matrix_from_points
import matplotlib.pyplot as plt
import math


def doMsg(msg):
    u,v=map(int,msg.data.split('_'))
    v0=np.array([u/2,v/2,0,1])
    v1 = np.dot(T_matrix,v0.T)
    print(v1)
    new_x=v1[0]
    new_y=v1[1]
    x,y,z=arm.positionQueryInMicrometers()
    arm.gotoPositionInmicrometers(int(new_x),int(new_y),zinit+50)
    pass



if __name__ == "__main__":

    arm=RobotSDK()
    arm.swichToRemoteControl()

    _,_,zinit=arm.positionQueryInMicrometers()

    T_matrix=np.array(
           [[ 3.49766354 ,-9.78307871e-2,  0.00000000,  3.60251951e+3],
            [-9.78307871e-2 ,-3.49766354e+0,  0.00000000e+0,  1.04175693e+3],
            [ 0.00000000e+0 , 0.00000000e+0, -3.49903145e+0,  0.00000000e+0],
            [ 0.00000000e+0,  0.00000000e+0,  0.00000000e+0,  1.00000000e+0]]
    )

    rospy.init_node("robot_control")
    sub = rospy.Subscriber("/image_view/clickuv", String, doMsg, queue_size=1)
    rospy.spin()




