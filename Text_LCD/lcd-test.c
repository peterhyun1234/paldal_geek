#include <wiringPi.h>           //WiringPi headers
#include <lcd.h>                //LCD headers from WiringPi
#include <stdio.h>              //Needed for the printf function below
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

//Pin numbers below are the WiringPi pin numbers
#define LCD_RS  25              //Register select pin
#define LCD_E   11              //Enable Pin
#define LCD_D4  26              //Data pin 4
#define LCD_D5  27              //Data pin 5
#define LCD_D6  28              //Data pin 6
#define LCD_D7  29              //Data pin 7

#define PORT 9000
#define IP   "192.168.1.134"
#define Initial "1: A Day Enroll\n2: Open"

void clear(int lcd)
{
    lcdClear(lcd);
    lcdPosition(lcd,0,0);
}

int main()
{
    int c_socket, len, n;
    struct sockaddr_in c_addr;
    int lcd;                //Handle for LCD
    char buf[1024];
    
    wiringPiSetup();        //Initialise WiringPi

    // Socket Connection Configure
    c_socket = socket(PF_INET, SOCK_STREAM, 0);

    memset(&c_addr, 0, sizeof(c_addr));
    c_addr.sin_addr.s_addr = inet_addr(IP);
    c_addr.sin_family = AF_INET;
    c_addr.sin_port = htons(PORT);

    // Socket Connection
    printf("Connect to %s...\n",IP);
    if(connect(c_socket, (struct sockaddr *) &c_addr, sizeof(c_addr)) == -1)
    {
        printf("Connection Error");
        close(c_socket);
        return -1;
    }

    //Initialise LCD(int rows, int cols, int bits, int rs, int enable, int d0, int d1, int d2, int d3, int d4, int d5, int d6, int d7)
    if (lcd = lcdInit (2, 16, 4, LCD_RS, LCD_E ,LCD_D4 , LCD_D5, LCD_D6,LCD_D7,0,0,0,0))
    {
        printf ("lcd init failed! \n");
        return -1 ;
    }
   
    clear(lcd);
    lcdPuts(lcd, Initial);

    while(1)
    {
        recv(c_socket, buf, sizeof(buf), 0);
        printf("%s\n",buf);
        if(buf[0] == '7')
        {
            //printf("Clear\n");
            clear(lcd);
        }
        else if(buf[0] == 'D')
        {
            //printf("Initial\n");
            clear(lcd);
            lcdPuts(lcd, Initial);
        }
        else
        {
            clear(lcd);
            lcdPuts(lcd, buf);
        }
        memset(buf,0,sizeof(buf));
        sleep(0.5);
    }
    close(c_socket);
}
