#!/usr/bin/env python

import socket
import rospy
from std_msgs.msg import Int32

def udp_listener():
    local_ip = "10.0.0.12"
    local_port = 4010
    # 终端设备的IP和端口
    device_ip = "10.0.0.11"
    device_port = 4010
    # 创建socket对象，使用UDP协议
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 发送第一个指令
    sock.sendto(b'\x01\x0A', (device_ip, device_port))
    data, addr = sock.recvfrom(1024)
    if data:print(data)
    # 发送第二个指令
    sock.sendto(b'\x01\x0A\x55', (device_ip, device_port))
    data, addr = sock.recvfrom(1024)
    if data:print(data)

    # 初始化ROS节点
    rospy.init_node('udp_listener_node', anonymous=True)

    # 创建ROS Publisher，将spectrum_data_10发布到名为'spectrum_data'的话题
    spectrum_data_pub = rospy.Publisher('/spectrum_data', Int32, queue_size=10)

    try:
        # i = 0
        while not rospy.is_shutdown():
            # 接收数据包
            data, addr = sock.recvfrom(1024)
            if not data:
                break
            
            data0 = hex(data[13])[2:]
            data1 = hex(data[12])[2:]
            data2 = hex(data[11])[2:]
            data3 = hex(data[10])[2:]
            
            if len(data0)==1:data0='0'+data0
            if len(data1)==1:data1='0'+data1
            if len(data2)==1:data2='0'+data2
            if len(data3)==1:data3='0'+data3
            
            spectrum_data_16_str = data0 + data1 + data2 + data3
            # 将16进制字符串转为整数
            spectrum_data_10 = int(spectrum_data_16_str, 16)
            # print(spectrum_data_10)

            # 发布spectrum_data_10到ROS话题
            spectrum_data_pub.publish(spectrum_data_10)

            # i += 1

    except rospy.ROSInterruptException:
        pass
    finally:
        # 关闭socket连接
        sock.close()

if __name__ == '__main__':
    try:
        udp_listener()
    except rospy.ROSInterruptException:
        pass
