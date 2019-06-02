#include <stdio.h>
#include <wiringPi.h>

#define MAG 4  //BCM 23번 

int main(void)
{
    int mag;

    if(wiringPiSetup() == -1)
        return 1;
    pinMode(MAG, INPUT);
    
    while(1)
    {
        mag = digitalRead(MAG);

        printf("mag = %d\n",mag);

        delay(1000);

    }

    return 0;
}
