#!/usr/bin/env python

import time
import rospy
from geometry_msgs.msg import PoseStamped
from omni_msgs.msg import OmniButtonEvent, OmniState
from robot_arm_control import RobotSDK



# TODO 机械臂发生抖动：1.速度控制 2.添加滤波器

def pose_callback_left(data):
    # rospy.loginfo("Received Pose: x={}, y={}, z={}".format(data.pose.position.x, data.pose.position.y, data.pose.position.z))

    global x0,y0,z0
    global x1,y1,z1
    s=0.5
    
    x=int(float(data.pose.position.x)*s)
    y=int(float(data.pose.position.y)*s)
    z=int(float(data.pose.position.z)*s)

    vx=int(float(data.velocity.x)*s)
    vy=int(float(data.velocity.y)*s)
    vz=int(float(data.velocity.z)*s)

    if x1 is None and  y1 is None and z1 is None:
        x1,y1,z1=x,y,z


    arm.gotoPositionInmicrometers_V(x0+(x-x1),y0+(y-y1),z0+(z-z1),vx,vy,vz)


    # 创建一个PoseStamped消息
    pose_stamped = PoseStamped()
    pose_stamped.header.stamp = rospy.Time.now()
    pose_stamped.header.frame_id = "left_micro"  # 指定参考坐标系
    pose_stamped.pose.position.x = x0+(x-x1)
    pose_stamped.pose.position.y = y0+(y-y1)
    pose_stamped.pose.position.z = z0+(z-z1)
    pub.publish(pose_stamped)
    

def pose_callback_right(data):
    # rospy.loginfo("Received Pose: x={}, y={}, z={}".format(data.pose.position.x, data.pose.position.y, data.pose.position.z))

    global x0,y0,z0
    global x1,y1,z1
    global pub
    s=0.5

    x=int(float(data.pose.position.x)*s)
    y=int(float(data.pose.position.y)*s)
    z=int(float(data.pose.position.z)*s)


    vx=int(float(data.velocity.x)*s)
    vy=int(float(data.velocity.y)*s)
    vz=int(float(data.velocity.z)*s)

    if x1 is None and  y1 is None and z1 is None:
        x1,y1,z1=x,y,z

    # arm.gotoPositionInmicrometersWithoutComplete(y0-(y-y1),x0+(x-x1),z0-(z-z1))
    arm.gotoPositionInmicrometers(y0-(y-y1),x0+(x-x1),z0-(z-z1),vy,vx,vz)


    # 创建一个PoseStamped消息
    pose_stamped = PoseStamped()
    pose_stamped.header.stamp = rospy.Time.now()
    pose_stamped.header.frame_id = "right_micro"  # 指定参考坐标系
    pose_stamped.pose.position.x = y0-(y-y1)
    pose_stamped.pose.position.y = x0+(x-x1)
    pose_stamped.pose.position.z = z0-(z-z1)
    pub.publish(pose_stamped)


def button_callback(data):
    rospy.loginfo("Received Button Event: Grey={}, White={}".format(data.grey_button, data.white_button))

def omni_state_callback(data):
    rospy.loginfo("Received Omni State: Locked={}, Close Gripper={}, Velocity: {}, {}, {}".format(
        data.locked, data.close_gripper, data.velocity.x, data.velocity.y, data.velocity.z))

def subscriber_node():

    global pose
    if 'left' in pose:
        rospy.loginfo('pose_callback_left')
        rospy.Subscriber(pose, OmniState, pose_callback_left,queue_size=1)
    else:
        rospy.loginfo('pose_callback_right')
        rospy.Subscriber(pose, OmniState, pose_callback_right,queue_size=1)
    rospy.spin()

if __name__ == "__main__":

    rospy.init_node('omni_subscriber_node', anonymous=True)  
    pub = rospy.Publisher('~micro_pose', PoseStamped, queue_size=1)

    port=rospy.get_param("~port")
    pose=rospy.get_param("~pose")
    rospy.loginfo(pose)
    rospy.loginfo(port)

    arm=RobotSDK(port)
    arm.swichToRemoteControl()
    if 'left' in pose:
        x0,y0,z0=arm.positionQueryInMicrometers()
    else:
        y0,x0,z0=arm.positionQueryInMicrometers()
    x1,y1,z1=None,None,None
    # print("(x0,y0,z0)",x0,y0,z0)
    subscriber_node()

