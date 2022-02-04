#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/device.h>
#include <linux/fs.h>

#include "myk.h"

/* Most operations are provided by ioctl() */
static long myk_ioctl (struct file * fd, unsigned int cmd, unsigned long arg){
  switch(cmd){
  
  
  
    /* Echo unsigned long in KERN_INFO level (only for test) */
    case MYK_CMD_ECHO:
      printk(KERN_INFO "myk: (ioctl) %ld\n", arg);
      return 0;
    default:
      printk(KERN_ALERT "myk: (ioctl) Invalid command\n");
      return -1;
  }
}


/* File operations */
static struct file_operations myk_ops = {
  .unlocked_ioctl = myk_ioctl
};


/* Kernel module init */
static int __init myk_init(void){
  int ret;
  ret = register_chrdev(297, "myk", &myk_ops);
  
  if (ret < 0){
    printk(KERN_ALERT "myk: Failed to register character device.\n");
    return ret;
  }
  

  printk(KERN_INFO "myk: Initialization completed.\n");
  return 0;
}

/* Kernel module exit */
static void __exit myk_exit(void){
  unregister_chrdev(297, "myk");

}

module_init(myk_init);
module_exit(myk_exit);

MODULE_LICENSE("WTFPL");
MODULE_AUTHOR("Eunseong Park / esp-ark.com");
MODULE_DESCRIPTION("My kernel practice");