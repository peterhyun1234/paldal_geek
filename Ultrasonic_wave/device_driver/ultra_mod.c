#include <linux/module.h>

#include <linux/kernel.h>

#include <linux/types.h>

#include <asm/io.h>

#include <linux/interrupt.h>

#include <linux/irq.h>

#include <linux/delay.h>

#include <linux/time.h>



#define GPIO_BASE      0xE0200000 // GPIO 기본주소

#define GPH0CON               (0xC00/4) // 사용할PIN의CONFIG 레지스터주소

#define GPH0DAT               (0xC04/4) // 사용할PIN의DATA 레지스터주소

#define IOCTL_MAGIC_NUMBER 'U'
#define IOCTL_ULTRA_REQ		_IO( IOCTL_MAGIC_NUMBER, 0)


MODULE_LICENSE("GPL");


#define TRIG        23 // TIR 핀의인덱스

#define ECHO		22 // ECHO 핀의인덱스



static volatile u32 *gpio_base = 0x0; // 주소를저장하는변수

struct timeval after, before; // 시간을계산하기위한변수

u32 irq; // 인터럽트등록을위한변수



static void gpio_data( int, int, int); // GPIO DATA 레지스터값을변경하는함수

static void gpio_config( int, int, int); // GPIO CONFIG 레지스터값을변경하는함수

int register_itrp( void); // 인터럽트처리함수

void gpio_init( void); // 기본적인GPIO PIN 초기화를하는함수

void output_sonicburst( void); // 펄스를발생시켜초음파를내보내게하는함수

float distance;

/*

   인터럽트처리함수



   - 초음파가되돌아와서ECHO 핀에신호가발생하면호출되는함수이다.

   - 현재시간을구해서이전시간과의차이로거리(cm)를계산한다.

 */

irqreturn_t int_interrupt( int irq, void *dev_id, struct pt_regs *regs)

{

	do_gettimeofday( &after);



	printk("%ldcm\n", (after.tv_usec - before.tv_usec) / 58);

	distance = ((after.tv_usec - before.tv_usec) / 58);

	return IRQ_HANDLED;

}

long ultra_ioctl( struct file *filp, unsigned int cmd, unsigned long arg)
{
	long value;

	if(cmd = IOCTL_ULTRA_REQ)
	{
		copy_to_user(value,sizeof(value));
	}

}


struct file operations fops = {
	.unlocked_ioctl = ultra_ioctl
}
/*

   모듈스타트함수



   - 모듈에커널에적재될때호출되는함수이다.

   - 기본적인초기화함수를호출한다. 메모리매핑, GPIO 설정, 인터럽트등록, 초음파발생

 */

int module_start( void)

{

	printk( "Ultra sonic device driver on!\n");



	gpio_base = (u32 *)ioremap( GPIO_BASE, PAGE_SIZE);



	gpio_init();



	register_itrp();



	while( 1)

	{

		output_sonicburst();

		mdelay(100);

	}

	return 0;

}



/*

   모듈엔드함수



   - 커널에서모듈이제거될때호출되는함수이다.

   - 메모리매핑해제, 인터럽트해제등마무리작업을수행한다.

 */

void module_end( void)

{

	if( gpio_base)

	{

		printk("upmapping address!\n");

		iounmap( (void*)gpio_base);

	}



	free_irq(irq, NULL);



	printk("devier driver off!\n");

}



/*

   인터럽트등록함수



   - 사용할인터럽트핀의정보를가져와서인터럽트를등록하는함수이다.

 */

int register_itrp( void)

{

	irq = IRQ_EINT(1);



	set_irq_type(irq, IRQ_TYPE_EDGE_FALLING);



	if( request_irq(irq, int_interrupt, IRQF_DISABLED, NULL, NULL))

	{

		return -EINVAL;

	}

	return 0;

}



/*

   초음파발생함수



   - 10uS 동안펄스를발생시켜서모듈에서초음파를보내도록한다.

 */

void output_sonicburst( void)

{

	gpio_data( GPH0DAT, TRIG, 1);

	udelay(10);

	gpio_data( GPH0DAT, TRIG, 0);



	do_gettimeofday( &before);

}



/*

   GPIO PIN 초기화함수



   - TRIG PIN은output으로ECHO PIN은interrupt로설정한다.

 */

void gpio_init( void)

{

	gpio_config( GPH0CON, TRIG, 1);

	gpio_config( GPH0CON, ECHO, 0xF);

}



/*

   GPIO DATA 레지스터값설정함수



   - 변경할레지스터의주소와값을받아, 값을변경한다.

   - DATA 레지스터의경우PIN 당1bit의크기를가진다.

 */

static void gpio_data( int gpio, int bit, int value)

{

	u32 data = 0x0;



	data = gpio_base[gpio];



	data &= ~(1 << bit);



	data |= (value << bit);



	gpio_base[gpio] = data;

}



/*

   GPIO CONFIG 레지스터값설정함수



   - 변경할레지스터의주소와값을받아, 값을변경한다.

   - CONFIG 레지스터의경우PIN 당4bit의크기를가진다.

 */

static void gpio_config( int gpio, int bit, int value)

{

	u32 data = 0x0;



	data = gpio_base[gpio];



	data &= (~(0xF << (bit * 4)));



	data |= (value << (bit * 4));



	gpio_base[gpio] = data;

}



module_init( module_start);

module_exit( module_end);




