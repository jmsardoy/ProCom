
#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"
#include "xuartlite.h"
#include "microblaze_sleep.h"

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
XUartLite uart_module;

//Funcion para recibir 1 byte bloqueante
//XUartLite_RecvByte((&uart_module)->RegBaseAddress)


int uart_receive(unsigned char *data, unsigned char *device){
    unsigned char header[3];
    unsigned char tail;
    unsigned int LS_flag;
    uint16_t data_length;

    header[0] = 0x00;
    while ((header[0]&(0xe0)) != 0xa0){
        read(stdin,&header[0],1);
    }
    read(stdin,&header[1],1);
    read(stdin,&header[2],1);
    read(stdin, device,1);

    LS_flag = (header[0]&0x10)>>4;
    if (LS_flag == 0){
        data_length = header[0]&0x0f;
    }
    else{
        data_length = (header[1]<<8)|header[2];
    }
    read(stdin, data, data_length);
    read(stdin, &tail, 1);

    if(tail == header[0]){
        return 0;
    }
    else{
        return -1;
    }
}

int uart_send(unsigned char *data, uint16_t length, unsigned char device){
    unsigned char header[3];
    unsigned char tail;
    
    header[0] = 0xa0;
    if (length>15){
        header[0] |= 0x10;
        header[1] = length>>8;
        header[2] = length&0xff;
    }
    else{
        header[0] |= length;
        header[1] = 0;
        header[2] = 0;
    }
    while(XUartLite_IsSending(&uart_module)){}
    XUartLite_Send(&uart_module, header,3);
    while(XUartLite_IsSending(&uart_module)){}
    XUartLite_Send(&uart_module, &(device),1);
    while(XUartLite_IsSending(&uart_module)){}
    XUartLite_Send(&uart_module, data,length);
    while(XUartLite_IsSending(&uart_module)){}
    XUartLite_Send(&uart_module, &(tail),1);

}

int main()
{
	init_platform();
	int Status;
	XUartLite_Initialize(&uart_module, 0);

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

    XGpio_DiscreteWrite(&GpioOutput,1, (u32) 0x00000000);
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
	
	cleanup_platform();
	return 0;
}
