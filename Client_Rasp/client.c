#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>
// For WiringPi
#include <wiringPi.h>
// For Socket Programming
#include <sys/ioctl.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define IOCTL_MAGIC_NUMBER	'L'
#define LED_ON  _IO( IOCTL_MAGIC_NUMBER, 0)
#define LED_OFF _IO( IOCTL_MAGIC_NUMBER, 1)

#define LP 26   // BCM 26, GPIO Pin 37, WPi 25 for LED
#define SV 0    // BCM 17, GPIO Pin 11, WPi 0 for Servo Motor

#define PORT 9000

int main(int argc, char ** argv)
{
    int c_socket, len, n;
    struct sockaddr_in c_addr;
	int fd_led = open("/dev/led_mod",O_RDWR);
    int led = -1;

    // Socket Connection Configure
    c_socket = socket(PF_INET,SOCK_STREAM,0);

    memset(&c_addr,0,sizeof(c_addr));
    c_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    c_addr.sin_family = AF_INET;
    c_addr.sin_port = htons(PORT);

    // LED Device Driver Open
    if( fd_led < 0 )
    {
        perror("Failed to open the device");
    }
    
    // WiringPi Setup For Servo Motor.
    wiringPiSetup();
    pinMode(SV, PWM_OUTPUT);
    pwmSetMode(PWM_MODE_MS);
    pwmSetRange(2000);
    pwmSetClock(192);

    // Socket Connection
    if(connect(c_socket,(struct sockaddr *) &c_addr, sizeof(c_addr)) == -1)
    {
        printf("Connection Error\n");
        close(c_socket);
        close(fd_led);
        return -1;
    }

    // Initialize LED Device
    // gpio_set_value(LP, HIGH);
    while(1)
    {
        scanf("%d",&led);
        if(led == 1)
        {
            ioctl(fd_led, IOCTL_LED_OFF, 0);
        }
        else if(led == 0)
        {
            ioctl(fd_led, IOCTL_LED_ON, 0);
        }

        // Servo Motor Actuation Code
        // pwmWrite(SV, 150);
        // pwmWrite(SV, 200);

        // For Socket Programming
        // send(c_socket, &but_value, sizeof(int), 0);

        sleep(1)
    }

	close(fd_led);
    close(c_socket);
	return 0;
}