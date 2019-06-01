#include <linux/init.h>
#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/fs.h>
#include <linux/kernel.h>
#include <linux/uaccess.h>

#define BN 8
#define B0 17   // 0
#define B1 18   // 1
#define B2 27   // 2
#define B3 22   // 3
#define B4 23   // 4
#define B5 24   // 5
#define BE 25   // 6 - Enter
#define BD 4    // 7 - Delete

MODULE_LICENSE("GPL");

#define IOCTL_MAGIC_NUMBER 'B'

#define IOCTL_BUTTON_REQ        _IO( IOCTL_MAGIC_NUMBER, 0)

static int gpios[BN] = {B0, B1, B2, B3, B4, B5, BE, BD};

long button_ioctl (struct file *filp, unsigned int cmd, unsigned long arg)
{
    int value[BN] = { 0, };
    if(cmd == IOCTL_BUTTON_REQ)
    {
        int index;
        for(index = 0; index < BN; index++)
        {
            value[index] = 1 - gpio_get_value(gpios[index]);
            // printk(KERN_INFO "Index %d: %d \n",index, value[index]);
            if(value[index] == 1)
            {
                printk(KERN_INFO "Send %d: %d \n",index, value[index]);
                copy_to_user((void*)arg, &index, sizeof(int));
                value[index] = 0;
                break;
            }
        }
    }
}

struct file_operations fops = {
	.unlocked_ioctl = button_ioctl
};

static int __init button_init(void)
{
	printk(KERN_INFO "Button : Starting ...\n");

	register_chrdev(241, "button_mod", &fops);


    gpio_request(B0, "B0");
    gpio_direction_input(B0);
    gpio_request(B1, "B1");
    gpio_direction_input(B1);
    gpio_request(B2, "B2");
    gpio_direction_input(B2);
    gpio_request(B3, "B3");
    gpio_direction_input(B3);
    gpio_request(B4, "B4");
    gpio_direction_input(B4);
    gpio_request(B5, "B5");
    gpio_direction_input(B5);
    gpio_request(BE, "BE");
    gpio_direction_input(BE);
    gpio_request(BD, "BD");
    gpio_direction_input(BD);


	printk(KERN_INFO "Button : Starting Complete\n");

	return 0;
}

static void __exit button_exit(void)
{
	gpio_free(B0);
	gpio_free(B1);
	gpio_free(B2);
	gpio_free(B3);
	gpio_free(B4);
    gpio_free(B5);
    gpio_free(BE);
    gpio_free(BD);
	unregister_chrdev(241, "button_mod");

	printk(KERN_INFO "Button : Exit Done");
}

module_init(button_init);
module_exit(button_exit);
