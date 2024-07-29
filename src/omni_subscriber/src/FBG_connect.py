#!/usr/bin/env python

import socket
import rospy
from std_msgs.msg import Int32

def udp_listener():

    device_ip = "10.0.0.11"
    device_port = 4010
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b'\x01\x0A', (device_ip, device_port))
    data, addr = sock.recvfrom(1024)
    if data:
        print(data)
    sock.sendto(b'\x01\x0A\x55', (device_ip, device_port))
    data, addr = sock.recvfrom(1024)
    if data:
        print(data)

    rospy.init_node('udp_listener_node', anonymous=True)

    spectrum_data_pub = rospy.Publisher('/spectrum_data', Int32, queue_size=10)

    try:
        while not rospy.is_shutdown():
            data, addr = sock.recvfrom(1024)
            # print('data:',data)
            if not data:
                break

            # For CH2

            data0 = hex(data[13])[2:]
            data1 = hex(data[12])[2:]
            data2 = hex(data[11])[2:]
            data3 = hex(data[10])[2:]


            if len(data0)==1:data0='0'+data0
            if len(data1)==1:data1='0'+data1
            if len(data2)==1:data2='0'+data2
            if len(data3)==1:data3='0'+data3
            
            spectrum_data_16_str = data0 + data1 + data2 + data3

            
            spectrum_data_10 = int(spectrum_data_16_str, 16)

            print(spectrum_data_16_str,spectrum_data_10)

            spectrum_data_pub.publish(spectrum_data_10)

            # break

            # i += 1

    except rospy.ROSInterruptException:
        pass
    finally:
        sock.close()

if __name__ == '__main__':
    # import sys
    # print(sys.executable)
    try:
        print("FBG connect!")
        udp_listener()
    except rospy.ROSInterruptException:
        pass
