#include <wiringPi.h>
#include <stdio.h>

#define BNUM 5

int butPin[BNUM] = {0,1,2,3,4};

void init_button()
{
    for(int i = 0; i < BNUM; i++)
    {
        pinMode(butPin[i], INPUT);
        pullUpDnControl(butPin[i], PUD_UP);
    }
}

int main(int argc, char **argv)
{
    wiringPiSetup();
    init_button();
    while(1)
    {
        int readBut[BNUM] = {-1,};
        for(int i = 0; i < BNUM; i++)
        {
            readBut[i] = digitalRead(butPin[i]);
        }
        printf("Button [%d, %d, %d, %d, %d]: [%d, %d, %d, %d, %d]\n",butPin[0], butPin[1], butPin[2], butPin[3], butPin[4], readBut[0], readBut[1], readBut[2], readBut[3], readBut[4]);
        delay(500);
    }
    return 0;
}
