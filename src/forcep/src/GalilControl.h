#ifndef GALILCONTROL_H
#define GALILCONTROL_H

#define _CRT_SECURE_NO_WARNINGS         //use traditional C calls like sprintf()

#include "gclib.h"
#include "gclibo.h"

#include <vector>
#include <tuple>
#include <ncurses.h>
#include <vector>
#include <string>
#include <math.h>
#include <iostream>

#define GALIL_EXAMPLE_OK 0              //return code for correct code execution
#define GALIL_EXAMPLE_ERROR -100        //return code for error in example code


inline void galil(GReturn rc)
{
    if (rc != G_NO_ERROR)
        throw rc;
    // std::cout<<"### galil"<<std::endl;
}

//! An example of error handling and debugging information.
inline void error(GCon g, GReturn rc)
{
    char buf[G_SMALL_BUFFER];
    GError(rc, buf, G_SMALL_BUFFER); //Get Error Information
    std::cout <<buf<<"\n";

    if (g)
    {
        GSize size = sizeof(buf);
        GUtility(g, G_UTIL_ERROR_CONTEXT, buf, &size);

        if (buf[0])
            printf(buf);
            printf("\n"); //further context

        if ((rc == G_BAD_RESPONSE_QUESTION_MARK)
            && (GCommand(g, "TC1", buf, G_SMALL_BUFFER, 0) == G_NO_ERROR))
        {
            printf(buf);
            printf("\n"); //Error code from controller
        }
    }
}
GReturn MainControl(GCon g);

void MainHomeCalibration(GCon g, std::vector<char> axis_list);
void MainForwardKinematics(GCon g);
void MainInverseKinematics(GCon g);
void MainPulseTest(GCon g);
void MainTurnOnMotor(GCon g, std::vector<char> axis_list);
void MainTurnOffMotor(GCon g, std::vector<char> axis_list);


GReturn ReadAnalog(GCon g, std::vector<double> &analog_info);
GReturn StopMotor(GCon g, char axis);
GReturn Jog(GCon g, char axis, int speed);
GReturn Jog(GCon g, char axis1, int speed1, char axis2, int speed2, char axis3, int speed3);
GReturn Jog(GCon g, char axis1, int speed1, char axis2, int speed2, char axis3, int speed3, char axis4, int speed4);
GReturn InitMotor(GCon g, char axis);
GReturn GoLimit(GCon g, char axis);
GReturn position_tracking(GCon g, char axis, int position, int speed);
GReturn GoPosition(GCon g, char axis, int pos, int speed);
GReturn DisableReverseLimit(GCon g, char axis);
GReturn SpaceMouseControl(GCon g, int speed);
//try to find edge to find zero point.
GReturn GoHome(GCon g, char axis);
GReturn GoHome2(GCon g, char axis);

#endif // GALILCONTROL_H
