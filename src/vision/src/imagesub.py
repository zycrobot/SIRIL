#! /home/microlab/anaconda3/envs/rosconda/bin/python

import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image

def image_callback(image_msg):
    cv2.namedWindow("imagesub",cv2.WINDOW_NORMAL)
    
    image_array = np.frombuffer(image_msg.data, dtype=np.uint8).reshape((image_msg.height, image_msg.width, -1))
    # 由于ROS默认的图像编码是'rgb8'，所以需要调整颜色通道的顺序为'BGR'
    image_array = image_array[:, :, [0, 1, 2]]

    cv2.imshow("imagesub", image_array)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        rospy.signal_shutdown("User quit")

def main():

    
    rospy.init_node('image_subscriber_node', anonymous=True)
 
    rospy.Subscriber('/image_raw', Image, image_callback)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")


    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()

