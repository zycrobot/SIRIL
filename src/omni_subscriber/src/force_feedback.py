#!/usr/bin/env python
import rospy
from omni_msgs.msg import OmniFeedback
import math

force = [0.0, 0.0, 0.0]  # Fx, Fy, Fz 
position = [0.0, 0.0, 0.0]  

def main():
    global force, position
    rospy.init_node('omni_feedback_publisher', anonymous=True)
    pub = rospy.Publisher('phantom/phantom/force_feedback', OmniFeedback, queue_size=10)
    rate = rospy.Rate(50)
    while not rospy.is_shutdown():
        feedback_msg = OmniFeedback()
        #TODO 接收FBG 波长信号，并转换为力反馈数据
        force = [0.0, 0.0, 0.8]  
        #位置信息实时获取，用于设置阻尼系统
        # position = [0.0, 0.0, 0.0] 
        feedback_msg.force.x, feedback_msg.force.y, feedback_msg.force.z = force
        feedback_msg.position.x, feedback_msg.position.y, feedback_msg.position.z = position
        pub.publish(feedback_msg)
        # print(feedback_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass