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
#include <pthread.h>
#include <softPwm.h>

#define IOCTL_MAGIC_NUMBER  'H'
#define IOCTL_LED_ON  _IO( IOCTL_MAGIC_NUMBER, 0)
#define IOCTL_LED_OFF _IO( IOCTL_MAGIC_NUMBER, 1)

#define PORT 9000
#define HOST "127.0.0.1"
#define IP "192.168.1.134"

#define LP      26  //BCM 26, GPIO Pin 37, WPi 25 for LED
#define SV      1   //BCM 18, GPIO Pin 12, WPi 1 for servo motor
#define MAG     4   //BCM 23, GPIO Pin 16, WPi 4 for magnetic_sensor


void *magnetic_sensor(void *arg);
void *control_door(void *arg);
void error_handling(char *msg);

static int door_state = 0;  //open : 1  

int main(int argc, char *argv[])
{

    int sock;
    struct sockaddr_in serv_addr;
    pthread_t control_t, magnetic_t;
    void * thread_return;


    sock=socket(PF_INET, SOCK_STREAM, 0);

    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family=AF_INET;
    serv_addr.sin_addr.s_addr=inet_addr(IP);
    serv_addr.sin_port=htons(PORT);

    if(connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr))==-1)
        error_handling("connect() error");

    pthread_create(&control_t, NULL, magnetic_sensor, (void*)&sock);
    pthread_create(&magnetic_t, NULL, control_door, (void*)&sock);
    pthread_join( control_t, &thread_return);
    pthread_join(magnetic_t, &thread_return);
    close(sock);  
    return 0;
}

void * control_door(void * arg)   // send thread main
{
    int sock=*((int*)arg);
    char cmd;
    
    wiringPiSetup();

    pinMode(SV, PWM_OUTPUT);

    digitalWrite(SV, LOW);
   
    softPwmCreate(SV, 0, 200);

    int fd_led = open("/dev/led_mod",O_RDWR);
    int led = -1;

    ioctl(fd_led, IOCTL_LED_OFF, 0); 
    while(1) 
    {
        // Initialize LED Device
        // gpio_set_value(LP, HIGH);
        recv(sock, &cmd, sizeof(char), 0);
        printf("cmd = %c\n", cmd);
        // Initialize "door close" and "LED off"
        // 사용중인 사물함은 LED on 으로 초기화 



        // control section about cmd
        if(cmd == 'O') // door open
        {
            softPwmWrite(SV, 24);
        }
        else if(cmd == 'C') // door close
        {
            softPwmWrite(SV, 5);
        }
        else if(cmd == 'N') //LED ON
        {
            ioctl(fd_led, IOCTL_LED_OFF, 0); 
        }
        else if(cmd == 'F') //LED OFF
        {
            ioctl(fd_led, IOCTL_LED_ON, 0);
        }

        sleep(1);
    }
    close(fd_led);
    return NULL;
}

void *magnetic_sensor(void * arg)   // read thread main
{
    int sock=*((int*)arg);
    char cmd;
    int mag;
    int cnt = 0;

    wiringPiSetup();
    pinMode(MAG, INPUT);

    while(1)
    {
        mag = digitalRead(MAG);     
        printf("mag = %d, cnt = %d\n", mag, cnt);
        if(mag == LOW) //door open
        {
            while(1)    //waiting for 5 minites
            {
                mag = digitalRead(MAG);
                printf("mag = %d, cnt = %d\n", mag, cnt);
                sleep(1);
                if(mag == HIGH)
                    break;

                if(cnt == 500)
                {
                    cmd = 'O';
                    send(sock, &cmd, sizeof(char),0);
                }
                cnt++;
            }
            cnt = 0;

        }
        sleep(1);
    }
    return NULL;
}

void error_handling(char *msg)
{
    fputs(msg, stderr);
    fputc('\n', stderr);
    exit(1);
}
