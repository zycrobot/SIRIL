#include <ros/ros.h>
#include <std_msgs/Int32.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <unistd.h>
#include <iostream>
#include <sstream>

void udpListener() {
    // 本地电脑的IP和端口
    std::string local_ip = "10.0.0.12";
    int local_port = 4010;
    // 终端设备的IP和端口
    std::string device_ip = "10.0.0.11";
    int device_port = 4010;
    // 创建socket对象，使用UDP协议
    int sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        ROS_ERROR("Failed to create socket");
        return;
    }

    struct sockaddr_in local_addr, device_addr;
    local_addr.sin_family = AF_INET;
    local_addr.sin_port = htons(local_port);
    local_addr.sin_addr.s_addr = inet_addr(local_ip.c_str());
    device_addr.sin_family = AF_INET;
    device_addr.sin_port = htons(device_port);
    device_addr.sin_addr.s_addr = inet_addr(device_ip.c_str());

    // 绑定本地地址
    if (bind(sock, (struct sockaddr *)&local_addr, sizeof(local_addr)) < 0) {
        ROS_ERROR("Failed to bind socket");
        close(sock);
        return;
    }

    // 发送第一个指令
    char command1[2] = {0x01, 0x0A};
    sendto(sock, command1, sizeof(command1), 0, (struct sockaddr *)&device_addr, sizeof(device_addr));
    char recv_buffer[1024];
    recvfrom(sock, recv_buffer, sizeof(recv_buffer), 0, NULL, NULL);
    if (recv_buffer[0])
        ROS_INFO_STREAM("Received: " << recv_buffer);

    // 发送第二个指令
    char command2[3] = {0x01, 0x0A, 0x55};
    sendto(sock, command2, sizeof(command2), 0, (struct sockaddr *)&device_addr, sizeof(device_addr));
    recvfrom(sock, recv_buffer, sizeof(recv_buffer), 0, NULL, NULL);
    if (recv_buffer[0])
        ROS_INFO_STREAM("Received: " << recv_buffer);

    // 创建ROS节点
    ros::NodeHandle nh;
    // 创建ROS Publisher，将spectrum_data_10发布到名为'spectrum_data'的话题
    ros::Publisher spectrum_data_pub = nh.advertise<std_msgs::Int32>("/spectrum_data", 10);

    try {
        while (ros::ok()) {
            // 接收数据包
            ssize_t bytes_received = recvfrom(sock, recv_buffer, sizeof(recv_buffer), 0, NULL, NULL);
            if (bytes_received <= 0)
                break;
            std::stringstream ss;
            for (ssize_t i = 13; i >= 10; --i) {
                ss << std::hex << std::setw(2) << std::setfill('0') << static_cast<int>(recv_buffer[i]);
            }
            int spectrum_data_10;
            ss >> spectrum_data_10;

            // 发布spectrum_data_10到ROS话题
            std_msgs::Int32 msg;
            msg.data = spectrum_data_10;
            spectrum_data_pub.publish(msg);
        }
    } catch (const std::exception& e) {
        ROS_ERROR_STREAM("Exception: " << e.what());
    } finally {
        // 关闭socket连接
        close(sock);
    }
}

int main(int argc, char** argv) {
    ros::init(argc, argv, "udp_listener_node");
    try {
        udpListener();
    } catch (const std::exception& e) {
        ROS_ERROR_STREAM("Exception: " << e.what());
    }
    return 0;
}
