#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define PORT 9000
#define IP  "192.168.28.41"
#define BUFSIZE 10

int main (int argc, char *argv[])
{

    int trig = 23 ;
    int echo = 22 ;
    int start_time, end_time ;
    float distance ;

    int c_socket, len, n, ultra_value = -1;
    struct sockaddr_in c_addr;

    // Socket Connection Configure
    c_socket = socket(PF_INET,SOCK_STREAM,0);

    memset(&c_addr,0,sizeof(c_addr));
    c_addr.sin_addr.s_addr = inet_addr(IP);
    c_addr.sin_family = AF_INET;
    c_addr.sin_port = htons(PORT);

    // Socket Connection
    printf("Connect to %s...\n",IP);
    if(connect(c_socket,(struct sockaddr *) &c_addr, sizeof(c_addr)) == -1)
    {
        printf("Connection Error\n");
        close(c_socket);
        return -1;
    }


    if (wiringPiSetup() == -1) exit(1) ;


    pinMode(trig, OUTPUT) ;
    pinMode(echo , INPUT) ;


    while(1) {

        digitalWrite(trig, LOW);
        delay(500);
        digitalWrite(trig, HIGH);
        delayMicroseconds(10) ;
        digitalWrite(trig, LOW);
        while (digitalRead(echo) == 0); //digitalRead가 false가 될때 까지 대기
        start_time = micros(); //프로그램이 시작된 후 흐른 시간
        while (digitalRead(echo) == 1); //
        end_time = micros() ;
        distance = (end_time - start_time) / 29. / 2. ; //시간의 차이를 이용해서 거리 도출
        // printf("distance:%f\n",distance);

	if(distance < 50)
        {
            ultra_value = 1;
            if(ultra_value != -1){
                char byte_value[BUFSIZE] = "";
                sprintf(byte_value, "%d", ultra_value);
		//printf("send_val:%s\n",byte_value);
                send(c_socket, byte_value, sizeof(byte_value), 0);
                ultra_value = -1;
            }
	}
	else{
	    ultra_value = 2;
            if(ultra_value != -1){
                char byte_value[BUFSIZE] = "";
                sprintf(byte_value, "%d", ultra_value);
		//printf("send_val:%s\n",byte_value);
                send(c_socket, byte_value, sizeof(byte_value), 0);
                ultra_value = -1;
            }

	}
    }
    close(c_socket);

    return 0 ;
}
