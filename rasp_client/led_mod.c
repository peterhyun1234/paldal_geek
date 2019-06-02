#include <linux/init.h>
#include <linux/module.h>
#include <linux/gpio.h>
#include <linux/fs.h>

// LED Device Driver 240

#define LP 26   // BCM 26, GPIO Pin 37, WPi 25 for LED

#define LOW 0
#define HIGH 1

MODULE_LICENSE("GPL");

#define IOCTL_MAGIC_NUMBER 'H'

#define IOCTL_LED_ON  _IO( IOCTL_MAGIC_NUMBER, 0)
#define IOCTL_LED_OFF _IO( IOCTL_MAGIC_NUMBER, 1)

long led_ioctl (struct file *filp, unsigned int cmd, unsigned long arg)
{
    switch(cmd)
    {
        case IOCTL_LED_ON : 
            gpio_set_value(LP, LOW);
            printk(KERN_INFO "LED : TURNNING ON LED\n");
            break;
        case IOCTL_LED_OFF : 
            gpio_set_value(LP, HIGH);
            printk(KERN_INFO "LED : TURNNING OFF LED\n");
            break;
    }
    return 0;
}

struct file_operations fops = {
    .unlocked_ioctl = led_ioctl
};

static int __init led_init(void)
{
    printk(KERN_INFO "LED : Starting ...\n");

    register_chrdev(240, "led_mod", &fops);

    gpio_request(LP, "LP");
    gpio_direction_output(LP, LOW);
    //gpio_set_value(LP, HIGH);

    printk(KERN_INFO "LED : Starting Complete\n");

    return 0;
}

static void __exit led_exit(void)
{
    gpio_free(LP);

    unregister_chrdev(240, "led_mod");

    printk(KERN_INFO "LED : Exit Done");
}

module_init(led_init);
module_exit(led_exit);
