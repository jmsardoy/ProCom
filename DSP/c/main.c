#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"
#include "microblaze_sleep.h"
#include "uart_manager/uart_manager.h"

#define PORT_IN	 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID

//Device_ID Operaciones
#define def_SOFT_RST            0
#define def_ENABLE_MODULES      1
#define def_LOG_RUN             2
#define def_LOG_READ            3


XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;
u32 GPO_Value;
u32 GPO_Param;


int main()
{
	init_platform();
	int Status;
    //uart_init();

	GPO_Value=0x00000000;
	GPO_Param=0x00000000;

	Status=XGpio_Initialize(&GpioInput, PORT_IN);
	if(Status!=XST_SUCCESS){
        return XST_FAILURE;
    }
	Status=XGpio_Initialize(&GpioOutput, PORT_OUT);
	if(Status!=XST_SUCCESS){
		return XST_FAILURE;
	}
	XGpio_SetDataDirection(&GpioOutput, 1, 0x00000000);
	XGpio_SetDataDirection(&GpioInput, 1, 0xFFFFFFFF);

    unsigned char data_in[256];
    unsigned char data_out[256];
    unsigned char device;

    u32 led_state = 0x00000000;
    u32 shift_mask =  0x00000007;
    u32 mask;
    uint8_t shift;
    uint8_t color;
    u32 switch_state;

    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000001);
    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00800001);
    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000001);

    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x01000003);
    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x01800003);
    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x01000003);

    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x02000003);
    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x02800003);
    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x02000003);

    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000000);
    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00800000);
    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000000);
    while(1){
        /*
        XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000000);
        XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00800000);
        XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000000);
        */
    }
    /*
    while(1){

        uart_receive(data_in, &device);
        if (device==0){
            shift = (data_in[0]>>4)*3;
            color = data_in[0]&0x07;
            mask = shift_mask<<shift;
            led_state &= (~mask);
            led_state |= color<<shift;
            XGpio_DiscreteWrite(&GpioOutput,1, led_state);
        }
        else if (device==1){
           switch_state = XGpio_DiscreteRead(&GpioInput, 1);
           data_out[0] = (char)(switch_state&(0x0000000F));
           uart_send(data_out, 1, 0);
        }
    }
    */
	
	cleanup_platform();
	return 0;
}
