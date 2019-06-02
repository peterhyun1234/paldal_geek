#include <stdio.h>
#include <wiringPi.h>
#include <softPwm.h>


#define servo  1

int main()
{
    //    char cmd;
    wiringPiSetup();
    
    pinMode(servo, PWM_OUTPUT);    //
    digitalWrite(servo, LOW);
    softPwmCreate(servo, 0, 200);   //intialize HIGH time 0ms, LOW time 200ms

    while(1)
    {
        softPwmWrite(servo, 24);
        delay(500);
 
        softPwmWrite(servo, 5); 
        delay(500);
    } 
    /*
    while(1)
    {
        cmd = getchar();
        printf("cmd : %c\n", cmd);
       
        if(cmd == 'D')  // +90 degree
        {
            softPwmWrite(GPI018, 5);
        }
        else if(cmd == 'R') // -90 degree
        {
            softPwmWrite(GPI018, 25);
        }
        else if(cmd == 'd') // -30 degree
        {
            softPwmWrite(GPI018, 5);
        }
        else if(cmd == 'r') // -30 degree
        {
            softPwmWrite(GPI018, 25);
        }
        else
            printf("I dont know what you command.\n");

        delay(100);
    }
    */

    return 0;
}
