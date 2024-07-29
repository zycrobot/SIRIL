#include <iostream>
#include <iomanip>
#include <string>
#include "GalilControl.h"
#include <time.h>
#include <unistd.h>
#include <chrono>
#include <ratio>
#include <linux/input.h>
#include <math.h>
#include <vector>

#include <ros/ros.h>
#include <geometry_msgs/PoseStamped.h>
#include <geometry_msgs/Wrench.h>
#include <geometry_msgs/WrenchStamped.h>
#include <urdf/model.h>
#include <sensor_msgs/JointState.h>

#include "omni_msgs/OmniButtonEvent.h"
#include "omni_msgs/OmniFeedback.h"
#include "omni_msgs/OmniState.h"

// gcc -o main main.cpp GalilControl.cpp  -lstdc++ -lgclib -lgclib -lgclibo -lncurses -lX11

using namespace std;

// void Forcep_SetServo(GCon g){
//     char buf[G_SMALL_BUFFER]; //traffic buffer
//     /*Initialize Motors*/
//     galil(GMotionComplete(g, "A")); //Wait for motion to complete
//     galil(GCmd(g, "SHA"));    // Set servo here
//     galil(GCmd(g, "DPA=0"));  // Start position at absolute zero
//     galil(GCmd(g, "JGA=0"));  // Start jogging with 0 speed
//     galil(GCmd(g, "BGA"));   // Begin motion on A Axis
//     galil(GCmd(g, "ACA=100000"));   // acceleration
//     galil(GCmd(g, "DCA=100000"));   // acceleration

//    return;

//}

GReturn Forcep(GCon g)
{
    char buf[G_SMALL_BUFFER]; // traffic buffer

    char forcep_axis = 'C';
    char rotate_axis = 'D';
    int position_hold = 6700; // TODO need calibration
    int position_release = 2500;
    int grasp_rotate_speed = 800;

    StopMotor(g, forcep_axis);

    GoHome2(g, forcep_axis); // first triggered photoelectric gate

    GoPosition(g, forcep_axis, position_release, grasp_rotate_speed); // then go to init position

    galil(GMotionComplete(g, "C")); // Wait for motion to complete
    galil(GCmd(g, "STC"));          // stop motor
    galil(GMotionComplete(g, "C")); // Wait for motion to complete
    // galil(GCmd(g, "DPC=0"));
    galil(GCmd(g, "PTC=1"));
    galil(GCmd(g, "SPC=1000"));  // speed
    galil(GCmd(g, "ACC=20000")); // acceleration
    galil(GCmd(g, "DCC=20000")); // deceleration

    // galil(GCmd(g, "PTD=1"));  // JOG is fail to work
    galil(GCmd(g, "SPD=1000"));  // speed
    galil(GCmd(g, "ACD=20000")); // acceleration
    galil(GCmd(g, "DCD=20000")); // deceleration
    galil(GCmd(g, "JGD=0"));     // set D axis Jog speed=0
    galil(GCmd(g, "BG D;"));     // Begin Jog
    std::cout << "option: 1--forcep clamping/2--forcep release/3--forcep rotating/else--stop rotating" << std::endl;

    int D_rotate_speed = 1000;
    //    int position_now = position_release;
    while (1)
    {
        // std::chrono::high_resolution_clock::time_point t1 = std::chrono::high_resolution_clock::now();

        /* GET INPUT */
        int option;
        std::cin >> option;
        std::cout << "option: " << option << std::endl;

        /* Forcep Control */
        if (option == 1)
        {
            sprintf(buf, "PA%c=%d", forcep_axis, position_hold);
            //            position_now+=20;
            //            sprintf(buf, "PA%c=%d",forcep_axis,position_now);
            galil(GCmd(g, buf)); // position relative
            std::cout << "clamping" << std::endl;
        }
        else if (option == 2)
        {
            sprintf(buf, "PA%c=%d", forcep_axis, position_release);
            //            position_now-=20;
            //            sprintf(buf, "PA%c=%d",forcep_axis,position_now);
            galil(GCmd(g, buf)); // position relative
            std::cout << "release" << std::endl;
        }
        // else if(option == 3){
        //     sprintf(buf, "PA%c=%d",rotate_axis,position_hold);

        //     galil(GCmd(g, buf)); // position relative
        //     std::cout << "rotate point1"<<std::endl;
        // }
        // else if(option == 4){
        //     sprintf(buf, "PA%c=%d",rotate_axis,position_release);

        //     galil(GCmd(g, buf)); // position relative
        //     std::cout << "rotate point2"<<std::endl;
        // }

        /* Rotate Control */
        if (option == 3)
        {
            Jog(g, 'D', 0);
            Jog(g, 'D', D_rotate_speed);
        }
        else if (option == 4)
        {
            Jog(g, 'D', 0);
            Jog(g, 'D', D_rotate_speed * -1);
        }
        else if (option == 5)
        {
            Jog(g, 'D', 0);
        }
        // loop end
        //        std::chrono::high_resolution_clock::time_point t2 = std::chrono::high_resolution_clock::now();
        //        std::chrono::duration<double> time_span = std::chrono::duration_cast<std::chrono::duration<double>>(t2 - t1);

        //        if(10000.0-time_span.count()*1000000>0){
        //            usleep(10000.0-time_span.count()*1000000);
        //        }
    }
    return GALIL_EXAMPLE_OK;
}

int main2()
{
    GReturn rc = GALIL_EXAMPLE_OK;
    char buf[G_SMALL_BUFFER];

    // var used to refer to a unique connection. A valid connection is nonzero.
    GCon g = 0;

    try
    {
        const char *address = "192.168.42.2"; // Retrieve address from command line
        // string address ="192.168.42.2";  //Retrieve address from command line
        sprintf(buf, "%s --subscribe MG", address);
        galil(GOpen(buf, &g)); // Opens a connection at the provided address

        rc = Forcep(g);
    }
    catch (GReturn gr)
    {
        error(g, gr); // see examples.h for error handling
        pause();
        return GALIL_EXAMPLE_ERROR;
    }

    pause();
    return GALIL_EXAMPLE_OK;
}

void joint_states_callback(const sensor_msgs::JointState::ConstPtr joint_states)
{
    // ROS_INFO("join = [%.3f] [%.3f] [%.3f] [%.3f] [%.3f] [%.3f]", joint_states->position[0], 
    // joint_states->position[1], joint_states->position[2], joint_states->position[3], 
    // joint_states->position[4], joint_states->position[5]);
    ;
}

void button_callback(const omni_msgs::OmniButtonEvent::ConstPtr button_states){
    ROS_INFO("white = [%d] gray = [%d]",button_states->white_button,button_states->grey_button);

}

int main(int argc, char *argv[])
{

    ros::init(argc, argv, "forcep_node");
    std::string joint_states_topic;
    ros::param::param(std::string("~joint_states_topic"), joint_states_topic, std::string("/left_device/phantom/joint_states"));
    ros::NodeHandle nh;
    ros::Subscriber joint_sub = nh.subscribe<sensor_msgs::JointState>(joint_states_topic.c_str(), 1, joint_states_callback);


    std::string button_topic;
    ros::param::param(std::string("~button_topic"), button_topic, std::string("/left_device/phantom/button"));
    ros::Subscriber button_sub = nh.subscribe<omni_msgs::OmniButtonEvent>(button_topic.c_str(), 10, button_callback);

    ros::spin();

    return 0;
}
