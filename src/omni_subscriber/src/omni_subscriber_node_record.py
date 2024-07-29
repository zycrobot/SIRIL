#!/usr/bin/env python


import rospy
from geometry_msgs.msg import PoseStamped
from omni_msgs.msg import OmniButtonEvent, OmniState


import datetime,time

def pose_callback(data):

    global filename
    x=str(float(data.pose.position.x))
    y=str(float(data.pose.position.y))
    z=str(float(data.pose.position.z))
    t=str(rospy.Time.now())
    txyz=t+" "+x+" "+y+" "+z
    rospy.loginfo("info:{}".format(txyz))

    with open(filename, 'a') as file:  
        file.write(txyz+"\n") 



def subscriber_node():
    rospy.init_node('omni_subscriber_node', anonymous=True)

    # Subscribe to Pose topic
    rospy.Subscriber('/phantom/pose', PoseStamped, pose_callback,queue_size=1)

    rospy.spin()


now_time = datetime.datetime.now()
str_time = now_time.strftime("%Y-%m-%d-%H-%M-%S")
filename="src/record20240326/"+str_time+'.txt'

with open(filename, 'w') as file:  
    pass

subscriber_node()

