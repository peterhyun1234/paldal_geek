#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <netinet/in.h>
#include <sys/socket.h>

#define IOCTL_MAGIC_NUMBER	'B'
#define IOCTL_BUTTON_REQ        _IO( IOCTL_MAGIC_NUMBER, 0)

#define BN 5
#define PORT 9000

int main(int argc, char ** argv)
{
    int c_socket, len, n, but_value = -1;
    struct sockaddr_in c_addr;
   
    // Socket Connection Configure
    socket = socket(PF_INET,SOCK_STREAM,0);

    memset(&c_addr,0,sizeof(c_addr));
    c_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    c_addr.sin_family = AF_INET;
    c_addr.sin_port = htons(Port);
    
    // Device Driver Connection
    int fd_but = open("/dev/button_mod",0_RDWR);
    if( fd_but < 0 )
    {
        perror("Failed to open the device");
        return -1;
    }
    
    // Socket Connection
    if(connect(c_socket,(struct sockaddr *) &c_addr, sizeof(c_addr)) == -1)
    {
        printf("Connection Error\n");
        close(c_socket);
        return -1;
    }

    while(1)
    {
        ioctl(fd_but, IOCTL_BUTTON_REQ, &but_value);
        
        if(but_value != -1)
        {
            send(c_socket, &but_value, sizeof(int), 0);
        }

        but_value = -1;
        sleep(1);    
    }

    close(fd_but);
    close(c_socket);
	return 0;
}
