#!/usr/bin/env python

import time
import rospy
from geometry_msgs.msg import PoseStamped
from omni_msgs.msg import OmniButtonEvent, OmniState
from robot_arm_control import RobotSDK

# TODO 机械臂发生抖动：1.速度控制 2.添加滤波器

def pose_callback_left(data):
    global x0,y0,z0
    global x1,y1,z1
    s=20 #set motion scale
    x=int(float(data.pose.position.x)*s)
    y=int(float(data.pose.position.y)*s)
    z=int(float(data.pose.position.z)*s)
    vx=abs(int(float(data.velocity.x)*s))
    vy=abs(int(float(data.velocity.y)*s))
    vz=abs(int(float(data.velocity.z)*s))
    #set speed contrain
    if vx>5000:vx=5000
    if vy>5000:vy=5000
    if vz>5000:vz=5000
    #init position
    if x1 is None and  y1 is None and z1 is None:
        x1,y1,z1=x,y,z
    #control
    arm.gotoPositionInmicrometers_V0(x0+(x-x1),y0+(y-y1),z0+(z-z1),vx,vy,vz)
    #record data
    state = OmniState()
    state.header.stamp = rospy.Time.now()
    state.header.frame_id = "left_micro" 
    state.pose.position.x = x0+(x-x1)
    state.pose.position.y = y0+(y-y1)
    state.pose.position.z = z0+(z-z1)
    state.velocity.x=vx
    state.velocity.y=vy
    state.velocity.z=vz
    pub.publish(state)
    
def pose_callback_right(data):
    # rospy.loginfo("Received Pose: x={}, y={}, z={}".format(data.pose.position.x, data.pose.position.y, data.pose.position.z))

    global x0,y0,z0
    global x1,y1,z1
    global pub
    s=20
    x=int(float(data.pose.position.x)*s)
    y=int(float(data.pose.position.y)*s)
    z=int(float(data.pose.position.z)*s)
    vx=abs(int(float(data.velocity.x)*s))
    vy=abs(int(float(data.velocity.y)*s))
    vz=abs(int(float(data.velocity.z)*s))
    if vx>5000:vx=5000
    if vy>5000:vy=5000
    if vz>5000:vz=5000
    if x1 is None and  y1 is None and z1 is None:
        x1,y1,z1=x,y,z
    # print('right',y0-(y-y1),x0+(x-x1),z0-(z-z1),vy,vx,vz)
    arm.gotoPositionInmicrometers_V0(y0-(y-y1),x0+(x-x1),z0-(z-z1),vy,vx,vz)
    state = OmniState()
    state.header.stamp = rospy.Time.now()
    state.header.frame_id = "right_micro"  # 指定参考坐标系
    state.pose.position.x = y0-(y-y1)
    state.pose.position.y = x0+(x-x1)
    state.pose.position.z = z0-(z-z1)
    state.velocity.x=vy
    state.velocity.y=vx
    state.velocity.z=vz
    pub.publish(state)

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
    pub = rospy.Publisher('~micro_pose', OmniState, queue_size=1)

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