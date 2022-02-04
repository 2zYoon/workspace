#include <sys/ioctl.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include "../myk.h"
int main(){
  int fd = open(MYK_CDEV_FNAME, O_RDWR);
  
  printf("[%d, %s]ret: %d\n", fd, MYK_CDEV_FNAME, ioctl(fd, MYK_CMD_ECHO, 278));
  return 0;
}