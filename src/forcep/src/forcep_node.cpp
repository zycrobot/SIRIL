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


GCon g = 0;
// gcc -o main main.cpp GalilControl.cpp  -lstdc++ -lgclib -lgclib -lgclibo -lncurses -lX11

// using namespace std;


GReturn Forcep_right_motor_init(GCon g){

    try{
        char buf[G_SMALL_BUFFER]; //traffic buffer
        char forcep_axis = 'C';
        // int position_hold = 8500;  //TODO need calibration
        int position_release =2100;
        int grasp_rotate_speed=1000;

        StopMotor(g, forcep_axis);
        GoHome2(g,forcep_axis);// first triggered photoelectric gate
        GoPosition(g,forcep_axis,position_release,grasp_rotate_speed);// then go to init position
        galil(GMotionComplete(g, "C")); //Wait for motion to complete
        galil(GCmd(g, "STC"));    // stop motor
        galil(GMotionComplete(g, "C")); //Wait for motion to complete
        galil(GCmd(g, "PTC=1"));
        galil(GCmd(g, "SPC=4000"));   // speed
        galil(GCmd(g, "ACC=20000"));   // acceleration
        galil(GCmd(g, "DCC=20000"));   // deceleration

        ROS_INFO("###axis C set");       
    }
    catch(...){
        ROS_INFO("### Wrong : axis C can't init");
    }


    try{
        char rotate_axis = 'D';
        int rotate_position1=2500;
        int rotate_position2=-2500;

        galil(GCmd(g, "SHD"));          // Set servo here
        galil(GCmd(g, "PTD=1"));        // Start position tracking mode on D axis
        galil(GCmd(g, "DPD=0"));        // Start position at absolute zero
        galil(GCmd(g, "SPD=2000"));   // speed
        galil(GCmd(g, "ACD=20000"));   // acceleration
        galil(GCmd(g, "DCD=20000"));   // deceleration
        ROS_INFO("###axis D set");
    }
    catch(...){
        ROS_INFO("### Wrong : axis D can't init");
    }



    return GALIL_EXAMPLE_OK;
}



GReturn Forcep_left_motor_init(GCon g){

    try{
        char buf[G_SMALL_BUFFER]; //traffic buffer
        char forcep_axis = 'A';
        // int position_hold = 8500;  //TODO need calibration
        int position_release =2100;
        int grasp_rotate_speed=1000;

        StopMotor(g, forcep_axis);
        GoHome2(g,forcep_axis);// first triggered photoelectric gate
        GoPosition(g,forcep_axis,position_release,grasp_rotate_speed);// then go to init position
        galil(GMotionComplete(g, "A")); //Wait for motion to complete
        galil(GCmd(g, "STA"));    // stop motor
        galil(GMotionComplete(g, "A")); //Wait for motion to complete
        galil(GCmd(g, "PTA=1"));
        galil(GCmd(g, "SPA=4000"));   // speed
        galil(GCmd(g, "ACA=20000"));   // acceleration
        galil(GCmd(g, "DCA=20000"));   // deceleration

        ROS_INFO("###axis A set");
    }
    catch(...){
        ROS_INFO("### Wrong : axis A can't init");
    }


    try{
        char rotate_axis = 'B';
        int rotate_position1=2500;
        int rotate_position2=-2500;

        galil(GCmd(g, "SHB"));          // Set servo here
        galil(GCmd(g, "PTB=1"));        // Start position tracking mode on D axis
        galil(GCmd(g, "DPB=0"));        // Start position at absolute zero
        galil(GCmd(g, "SPB=2000"));   // speed
        galil(GCmd(g, "ACB=20000"));   // acceleration
        galil(GCmd(g, "DCB=20000"));   // deceleration

        ROS_INFO("###axis B set"); 
    }
    catch(...){
        ROS_INFO("### Wrong : axis B can't init");
    }




    return GALIL_EXAMPLE_OK;
}



int gcConnection()
{
    GReturn rc = GALIL_EXAMPLE_OK;
    char buf[G_SMALL_BUFFER];
    try
    {
        const char *address = "192.168.42.2"; // Retrieve address from command line
        sprintf(buf, "%s --subscribe MG", address);
        galil(GOpen(buf, &g)); // Opens a connection at the provided address
    }
    catch (GReturn gr)
    {
        error(g, gr); // see examples.h for error handling
        ROS_INFO("### 192.168.42.2 connection failed!");
        return GALIL_EXAMPLE_ERROR;
    }
    return GALIL_EXAMPLE_OK;
}

void left_joint_states_callback(const sensor_msgs::JointState::ConstPtr joint_states)
{
    // ROS_INFO("join = [%.3f] [%.3f] [%.3f] [%.3f] [%.3f] [%.3f]", joint_states->position[0], 
    // joint_states->position[1], joint_states->position[2], joint_states->position[3], 
    // joint_states->position[4], joint_states->position[5]);
    // ;

    return;

    const double min_angle = -5.753408;
    const double max_angle = -0.524877;
    const double encode_half = 2500;

    double angle =joint_states->position[5];

    int encoder_value = static_cast<int>(((angle - min_angle) / (max_angle-min_angle)) *2*encode_half + (-1*encode_half));

    ROS_INFO("left::goto = [%d]",encoder_value);

    char buf[G_SMALL_BUFFER]; //traffic buffer
    char rotate_axis = 'B';

    sprintf(buf, "PA%c=%d",rotate_axis,encoder_value);
    galil(GCmd(g, buf)); // position relative
    // galil(GMotionComplete(g, "D")); //Wait for motion to complete
    std::cout << "left::rotate!!"<<std::endl;


}

void left_button_callback(const omni_msgs::OmniButtonEvent::ConstPtr button_states){

    return;


    ROS_INFO("left::white = [%d] gray = [%d]",button_states->white_button,button_states->grey_button);

    char buf[G_SMALL_BUFFER]; //traffic buffer
    char forcep_axis = 'A';

    int position_hold = 8000;  //TODO need calibration
    int position_release =2100;

    if(button_states->white_button==0&button_states->grey_button==1){
        sprintf(buf, "PA%c=%d",forcep_axis,position_hold);
        galil(GCmd(g, buf)); // position relative
        // galil(GMotionComplete(g, "C")); //Wait for motion to complete
        std::cout << "left::clamping"<<std::endl;
    }
    else{
        sprintf(buf, "PA%c=%d",forcep_axis,position_release);
        galil(GCmd(g, buf)); // position relative
        // galil(GMotionComplete(g, "C")); //Wait for motion to complete
        std::cout << "left::release"<<std::endl;
    }


}

void right_joint_states_callback(const sensor_msgs::JointState::ConstPtr joint_states)
{
    // ROS_INFO("right joint = [%.3f] [%.3f] [%.3f] [%.3f] [%.3f] [%.6f]", joint_states->position[0], 
    // joint_states->position[1], joint_states->position[2], joint_states->position[3], 
    // joint_states->position[4], joint_states->position[5]);
    // ;

    // return ;


    const double min_angle = -5.753408;
    const double max_angle = -0.524877;
    const double encode_half = 2500;

    double angle =joint_states->position[5];

    int encoder_value = static_cast<int>(((angle - min_angle) / (max_angle-min_angle)) *2*encode_half + (-1*encode_half));

    // ROS_INFO("right::goto = [%d]",encoder_value);

    char buf[G_SMALL_BUFFER]; //traffic buffer
    char rotate_axis = 'D';

    sprintf(buf, "PA%c=%d",rotate_axis,encoder_value);
    galil(GCmd(g, buf)); // position relative
    // galil(GMotionComplete(g, "D")); //Wait for motion to complete
    // std::cout << "right::rotate!!"<<std::endl;


}

void right_button_callback(const omni_msgs::OmniButtonEvent::ConstPtr button_states){
    ROS_INFO("right::white = [%d] gray = [%d]",button_states->white_button,button_states->grey_button);

    // return;

    char buf[G_SMALL_BUFFER]; //traffic buffer
    char forcep_axis = 'C';

    int position_hold = 8000;  //TODO need calibration
    int position_release =2100;

    if(button_states->white_button==0&button_states->grey_button==1){
        sprintf(buf, "PA%c=%d",forcep_axis,position_hold);
        galil(GCmd(g, buf)); // position relative
        // galil(GMotionComplete(g, "C")); //Wait for motion to complete
        std::cout << "right::clamping"<<std::endl;
    }
    else{
        sprintf(buf, "PA%c=%d",forcep_axis,position_release);
        galil(GCmd(g, buf)); // position relative
        // galil(GMotionComplete(g, "C")); //Wait for motion to complete
        std::cout << "right::release"<<std::endl;
    }

}

int main(int argc, char *argv[])
{

    ros::init(argc, argv, "forcep_node");
    ros::NodeHandle nh;

    std::string joint_states_topic;
    std::string button_topic;

    ros::param::param(std::string("~joint_states_topic"), joint_states_topic, std::string("/left_device/phantom/joint_states"));
    ros::param::param(std::string("~button_topic"), button_topic, std::string("/left_device/phantom/button"));
    ROS_INFO("###joint_states_topic:%s",joint_states_topic.c_str());   
    ROS_INFO("###button_topic:%s",button_topic.c_str());   


    if(joint_states_topic.find("left") != std::string::npos){ //"left" in joint_states_topic
        ROS_INFO("###left subscribe");

        // gcConnection();
        // Forcep_left_motor_init(g);

        ros::Subscriber joint_sub = nh.subscribe<sensor_msgs::JointState>(joint_states_topic.c_str(), 1, left_joint_states_callback);
        ros::Subscriber button_sub = nh.subscribe<omni_msgs::OmniButtonEvent>(button_topic.c_str(), 1, left_button_callback);
        ros::spin();
    }
    else if(joint_states_topic.find("right") != std::string::npos){ //"right" in joint_states_topic
        ROS_INFO("###right subscribe");
        gcConnection();
        Forcep_right_motor_init(g);
        
        ros::Subscriber joint_sub = nh.subscribe<sensor_msgs::JointState>(joint_states_topic.c_str(), 1, right_joint_states_callback);
        ros::Subscriber button_sub = nh.subscribe<omni_msgs::OmniButtonEvent>(button_topic.c_str(), 1, right_button_callback);
        ros::spin();
    }

    

    return GALIL_EXAMPLE_OK;
}


