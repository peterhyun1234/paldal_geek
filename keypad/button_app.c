#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>

#define IOCTL_MAGIC_NUMBER	'B'
#define IOCTL_BUTTON_REQ        _IO( IOCTL_MAGIC_NUMBER, 0)

#define BN 5

int main(int argc, char ** argv)
{
    int fd_but = open("/dev/button_mod",O_RDWR);
    int but_value = -1;

    if( fd_but < 0 )
    {
        perror("Failed to open the device");
        return -1;
    }
    
    while(1)
    {
        ioctl(fd_but, IOCTL_BUTTON_REQ, &but_value);
        printf("Input: %d\n",but_value);
        but_value = -1;
        sleep(1);    
    }

    close(fd_but);
	return 0;
}
