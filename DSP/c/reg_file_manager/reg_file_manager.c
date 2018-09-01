#include "reg_file_manager.h"

#define PORT_IN	 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID

void reg_file_init(){
	int Status;

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
}

void reg_file_write(u32 op_type, u32 opcode, u32 data){
    u32 enable_mask = 0x00800000;
    opcode = (op_type << 6) | opcode;
    u32 instruction = (opcode << 24) | data;
    
    XGpio_DiscreteWrite(&GpioOutput, 1, instruction);
    XGpio_DiscreteWrite(&GpioOutput, 1, instruction | enable_mask);
    XGpio_DiscreteWrite(&GpioOutput, 1, instruction);
}

u32 reg_file_read(){
    u32 out = XGpio_DiscreteRead(&GpioInput, 1);
    return out;
}
