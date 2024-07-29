#! /home/microlab/anaconda3/envs/rosconda/bin/python

from pickle import GLOBAL
import numpy as np
import rospy
from std_msgs.msg import String
from robot_arm_control import RobotSDK
from transformations import affine_matrix_from_points
import matplotlib.pyplot as plt
import math

SLEEP=4
DELTA=20

def doMsg(msg):
    global i
    global tiptj
    global imgtj
    if i>=40:
        sub.unregister()
        return

    # rospy.loginfo("接收到的数据：%s", msg.data)
    u,v=map(int,msg.data.split('_'))
    rospy.loginfo("i:%s",i)

    x0,y0,z0=arm.positionQueryInMicrometers()
    rospy.loginfo("x:%s,y:%s",x0,y0)
    rospy.loginfo("u:%s,v:%s",u,v)

    tiptj.append([x0,y0,0])
    imgtj.append([u,v,0])

    

    if i>=0 and i<10:
        arm.gotoPositionInmicrometers(x0+DELTA,y0,z0)
        x0,y0,z0=arm.positionQueryInMicrometers()

    elif i>=10 and i<20:
        arm.gotoPositionInmicrometers(x0,y0+DELTA,z0)
        x0,y0,z0=arm.positionQueryInMicrometers()

    elif i>=20 and i<30:
        arm.gotoPositionInmicrometers(x0-DELTA,y0,z0)
        x0,y0,z0=arm.positionQueryInMicrometers()


    elif i>=30 and i<40:
        arm.gotoPositionInmicrometers(x0,y0-DELTA,z0)
        x0,y0,z0=arm.positionQueryInMicrometers()
    i+=1

    rospy.sleep(4)

def doMsg2(msg):
    global i
    global tiptj
    global imgtj
    if i>=40:
        sub.unregister()
        return

    # rospy.loginfo("接收到的数据：%s", msg.data)
    u,v=map(int,msg.data.split('_'))
    rospy.loginfo("i:%s",i)

    x0,y0,z0=arm.positionQueryInMicrometers()
    rospy.loginfo("x:%s,y:%s",x0,y0)
    rospy.loginfo("u:%s,v:%s",u,v)

    tiptj.append([x0,y0,0])
    imgtj.append([u,v,0])


    # if i>=0 and i<10:
    arm.gotoPositionInmicrometers(point_list[i][0],point_list[i][1],z0)
    x0,y0,z0=arm.positionQueryInMicrometers()

    # elif i>=10 and i<20:
    #     arm.gotoPositionInmicrometers(x0,y0+DELTA,z0)
    #     x0,y0,z0=arm.positionQueryInMicrometers()
        
    # elif i>=20 and i<30:
    #     arm.gotoPositionInmicrometers(x0-DELTA,y0,z0)
    #     x0,y0,z0=arm.positionQueryInMicrometers()


    # elif i>=30 and i<40:
    #     arm.gotoPositionInmicrometers(x0,y0-DELTA,z0)
    #     x0,y0,z0=arm.positionQueryInMicrometers()


    i+=1

    rospy.sleep(6)
    

if __name__ == "__main__":


    i=0
    tiptj=[]
    imgtj=[]
    arm=RobotSDK()
    arm.swichToRemoteControl()


    a,b,_=arm.positionQueryInMicrometers()   #圆点坐标
    w = 40  # 圆平均分为10份
    m = (2*math.pi)/w #一个圆分成10份，每一份弧度为 m
    r = 300  #半径
    point_list = []
    for j in range(0, w+1):
        x = a+r*math.sin(m*j)
        y = b+r*math.cos(m*j)
        point_list.append([int(x),int(y)])


    rospy.init_node("initcalibration")
    sub = rospy.Subscriber("/image_view/detectuv", String, doMsg2, queue_size=1)

    while True:
        if i>=40:
            log = open("a.txt",mode="a",encoding="utf-8")
            tiptj=np.array(tiptj)
            imgtj=np.array(imgtj)
            print(tiptj)
            # print('\n',file=log)
            print(imgtj)
            # print('\n',file=log)
            M=affine_matrix_from_points(imgtj.T,tiptj.T,shear=False,scale=True,usesvd=False)
            print(M)
            # print('\n',file=log)
            R=M[:3,:3]
            T=M[:3,3]
            transimg=R@imgtj.T+T.reshape(3,1);
            plt.plot(transimg[0,:],transimg[1,:],'ro',label='QT')
            plt.plot(tiptj[:,0],tiptj[:,1],'b*',label='robot')
            plt.legend([''])
            plt.xlabel('x')
            plt.ylabel('y')
            ax = plt.gca()
            ax.set_aspect(1)
            plt.show()
            error=np.linalg.norm(transimg-tiptj.T)/tiptj.shape[0]
            print(">>>error=",error)
            log.close()
            break
        else:
            pass

    rospy.spin()


