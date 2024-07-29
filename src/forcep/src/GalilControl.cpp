#include "GalilControl.h"

GReturn InitMotor(GCon g, char axis)
{
    char buf[G_SMALL_BUFFER];

    sprintf(buf, "AG%c=0", axis);
    galil(GCmd(g, buf));

    sprintf(buf, "AU%c=0.5", axis);
    galil(GCmd(g, buf));

    sprintf(buf, "TL%c=3", axis);
    galil(GCmd(g, buf));

    sprintf(buf, "TK%c=8", axis);
    galil(GCmd(g, buf));

    sprintf(buf, "BR%c=1", axis);
    galil(GCmd(g, buf));

    sprintf(buf, "ST%c", axis);
    galil(GCmd(g, buf));

    sprintf(buf, "SH%c", axis);
    galil(GCmd(g, buf));

    return GALIL_EXAMPLE_OK;
}
GReturn GoHome(GCon g, char axis)
{
    int speed = 200000, acc = 40000000;
    char buf[G_SMALL_BUFFER];

    if (axis == 'A')
    {
        speed = -25000;
    }
    sprintf(buf, "SH%", axis);
    galil(GCmd(g, buf)); // Set servo

    sprintf(buf, "SP%c=%d", axis, speed);
    galil(GCmd(g, buf)); // Set speed

    sprintf(buf, "AC%c=%d", axis, acc);
    galil(GCmd(g, buf)); // Set acceleration

    sprintf(buf, "DC%c=%d", axis, acc);
    galil(GCmd(g, buf)); // Set deceleration
    printf("axis %c speed is set. Going to Home position\n", axis);

    sprintf(buf, "FE%c", axis);
    galil(GCmd(g, buf)); // Find Edge

    sprintf(buf, "BG%c", axis);
    galil(GCmd(g, buf)); // Begin Motion

    sprintf(buf, "%c", axis);
    galil(GMotionComplete(g, buf)); // Wait for motion to complete

    printf("axis %c is at home.\n", axis);

    return GALIL_EXAMPLE_OK;
}
GReturn GoHome2(GCon g, char axis)
{

    int speed = 1000, acc = 20000;
    char buf[G_SMALL_BUFFER];

    if (axis == 'C')
    {
        speed = 1000;
    }
    sprintf(buf, "SH%", axis);
    galil(GCmd(g, buf)); // Set servo

    sprintf(buf, "SP%c=%d", axis, speed);
    galil(GCmd(g, buf)); // Set speed

    sprintf(buf, "AC%c=%d", axis, acc);
    galil(GCmd(g, buf)); // Set acceleration

    sprintf(buf, "DC%c=%d", axis, acc);
    galil(GCmd(g, buf)); // Set deceleration
    printf("axis %c speed is set. Going to Home position\n", axis);

    sprintf(buf, "CN ,1");
    galil(GCmd(g, buf)); // Find Edge

    sprintf(buf, "FE%c", axis);
    galil(GCmd(g, buf)); // Find Edge

    sprintf(buf, "BG%c", axis);
    galil(GCmd(g, buf)); // Begin Motion

    sprintf(buf, "%c", axis);
    galil(GMotionComplete(g, buf)); // Wait for motion to complete

    printf("axis %c is at home.\n", axis);

    return GALIL_EXAMPLE_OK;
}
GReturn position_tracking(GCon g, char axis, int position, int speed)
{
    char buf[G_SMALL_BUFFER]; // traffic buffer
    int acc = 100 * speed;    // set acceleration/deceleration to 100 times speed

    if (g == 0) // Bad connection
    {
        printf("There was an error with the connection.\n");
        return G_CONNECTION_NOT_ESTABLISHED;
    }

    galil(GCmd(g, "STA"));          // stop motor
    galil(GMotionComplete(g, "A")); // Wait for motion to complete
    galil(GCmd(g, "SHA"));          // Set servo here
    galil(GCmd(g, "DPA=0"));        // Start position at absolute zero
    galil(GCmd(g, "PTA=1"));        // Start position tracking mode on A axis

    sprintf(buf, "SPA=%d", speed);
    galil(GCmd(g, buf)); // Set speed

    sprintf(buf, "ACA=%d", acc);
    galil(GCmd(g, buf)); // Set acceleration

    sprintf(buf, "DCA=%d", acc);
    galil(GCmd(g, buf)); // Set deceleration

    // Loop asking user for new position.  End loop when user enters a non-number
    while (1)
    {
        sprintf(buf, "PAA=%d", position);
        galil(GCmd(g, buf)); // Go to new position
    }

    galil(GCmd(g, "STA"));          // stop motor
    galil(GMotionComplete(g, "A")); // Wait for motion to complete

    return GALIL_EXAMPLE_OK;
}
GReturn GoPosition(GCon g, char axis, int position, int speed)
{

    char buf[G_SMALL_BUFFER];

    sprintf(buf, "SP%c=%d", axis, speed);
    galil(GCmd(g, buf));

    sprintf(buf, "DP%c=0", axis);
    galil(GCmd(g, buf)); // define the current position as zero

    sprintf(buf, "PR%c=%d", axis, position);
    galil(GCmd(g, buf)); // position relative

    sprintf(buf, "BG%c", axis);
    galil(GCmd(g, buf)); // begin

    sprintf(buf, "%c", axis);
    galil(GMotionComplete(g, buf));

    printf("axis %c is at init position.\n", axis);
    /*
        int acc = 100*speed;

        sprintf(buf, "ST%c", axis);
        galil(GCmd(g, buf));    // stop motor

        sprintf(buf, "%c", axis);
        galil(GMotionComplete(g, buf)); //Wait for motion to complete

        sprintf(buf, "SH%c", axis);
        galil(GCmd(g, "SH%c"));   // Set servo here

        sprintf(buf, "DP%c=0", axis);
        galil(GCmd(g, "DP%c=0")); // Start position at absolute zero

        sprintf(buf, "PT%c=1", axis);
        galil(GCmd(g, "buf")); // Start position tracking mode on the axis

        sprintf(buf, "SP%c=%d",axis, speed);
        galil(GCmd(g, buf)); // Set speed

        sprintf(buf, "AC%c=%d",axis, acc);
        galil(GCmd(g, buf)); // Set acceleration

        sprintf(buf, "DC%c=%d",axis, acc);
        galil(GCmd(g, buf)); // Set deceleration

        while(1){
            std::cout <<position << std::endl;
            sprintf(buf, "PA%c=%d",axis, position);
            galil(GCmd(g, buf)); // Go to new position

        }

        sprintf(buf, "ST%c=%d",axis, acc);
        galil(GCmd(g, buf)); //stop motor

        sprintf(buf, "%c", axis);
        galil(GMotionComplete(g, buf)); //Wait for motion to complete

    */
    return GALIL_EXAMPLE_OK;
}

GReturn Jog(GCon g, char axis, int speed = 0)
{
    char buf[G_SMALL_BUFFER];
    
    // galil(GCmd(g, "JG ,,2000;"));
    sprintf(buf, "JG%c=%d", axis, speed);
    // std::cout<<axis<<" "<<speed<<std::endl;

    galil(GCmd(g, buf)); // Set speed
    return GALIL_EXAMPLE_OK;
}
GReturn StopMotor(GCon g, char axis)
{
    char buf[G_SMALL_BUFFER];
    sprintf(buf, "ST%c", axis);
    galil(GCmd(g, buf));

    sprintf(buf, "%c", axis);
    galil(GMotionComplete(g, buf));

    sprintf(buf, "MO%c", axis);
    galil(GCmd(g, buf));

    return GALIL_EXAMPLE_OK;
}
GReturn Jog(GCon g, char axis1, int speed1, char axis2, int speed2, char axis3, int speed3)
{

    char buf1[G_SMALL_BUFFER];
    char buf2[G_SMALL_BUFFER];
    char buf3[G_SMALL_BUFFER];

    sprintf(buf1, "JG%c=%d", axis1, speed1);
    sprintf(buf2, "JG%c=%d", axis2, speed2);
    sprintf(buf3, "JG%c=%d", axis3, speed3);

    galil(GCmd(g, buf1)); // Set speed
    galil(GCmd(g, buf2)); // Set speed
    galil(GCmd(g, buf3)); // Set speed

    return GALIL_EXAMPLE_OK;
}
GReturn Jog(GCon g, char axis1, int speed1, char axis2, int speed2, char axis3, int speed3, char axis4, int speed4)
{

    char buf1[G_SMALL_BUFFER];
    char buf2[G_SMALL_BUFFER];
    char buf3[G_SMALL_BUFFER];
    char buf4[G_SMALL_BUFFER];

    sprintf(buf1, "JG%c=%d", axis1, speed1);
    sprintf(buf2, "JG%c=%d", axis2, speed2);
    sprintf(buf3, "JG%c=%d", axis3, speed3);
    sprintf(buf4, "JG%c=%d", axis4, speed4);

    galil(GCmd(g, buf1)); // Set speed
    galil(GCmd(g, buf2)); // Set speed
    galil(GCmd(g, buf3)); // Set speed
    galil(GCmd(g, buf4)); // Set speed

    return GALIL_EXAMPLE_OK;
}

GReturn ReadAnalog(GCon g, std::vector<double> &analog_info)
{
    char buf[G_SMALL_BUFFER]; // traffic buffer
    double tmp1, tmp2, tmp3, tmp4;
    while (1)
    {
        galil(GCmdD(g, "MG @AN[1]", &tmp1));
        galil(GCmdD(g, "MG @AN[2]", &tmp2));
        galil(GCmdD(g, "MG @AN[3]", &tmp3));
        galil(GCmdD(g, "MG @AN[4]", &tmp4));
    }
    analog_info[0] = tmp1;
    analog_info[1] = tmp2;
    analog_info[2] = tmp3;
    analog_info[3] = tmp4;

    return GALIL_EXAMPLE_OK;
}
