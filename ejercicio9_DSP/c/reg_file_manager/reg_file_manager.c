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
    out = XGpio_DiscreteRead(&GpioInput, 1);
    out = XGpio_DiscreteRead(&GpioInput, 1);
    return out;
}


void read_ber_counter(uint64_t * bit_error_re, uint64_t * bit_count_re, uint64_t * bit_error_im, uint64_t  * bit_count_im){
    u32 reg_file_out;

    reg_file_write(COUNT_LOG_OP_TYPE,BER_LATCH_CODE,0); //rf latchea los dos contadores de ber

    *bit_count_re = 0;
    *bit_error_re = 0;
    *bit_count_im = 0;
    *bit_error_im = 0;


    //////////////////////////////contador de bits real///////////////////////////
    reg_file_write(COUNT_LOG_OP_TYPE,BIT_COUNT_RE_HIGH_CODE,0);//leo parte alta del contador de bit 
    reg_file_out = reg_file_read();
    *bit_count_re |= ((uint64_t) reg_file_out) << 32;
    reg_file_write(COUNT_LOG_OP_TYPE,BIT_COUNT_RE_LOW_CODE,0);//leo parte baja del contador de bit 
    reg_file_out = reg_file_read();
    *bit_count_re |= ((uint64_t) reg_file_out);

    /////////////////////////////contador de bits imaginario/////////////////////////
    reg_file_write(COUNT_LOG_OP_TYPE,BIT_COUNT_IM_HIGH_CODE,0);//leo parte alta del contador de bit 
    reg_file_out = reg_file_read();
    *bit_count_im |= ((uint64_t) reg_file_out) << 32;
    reg_file_write(COUNT_LOG_OP_TYPE,BIT_COUNT_IM_LOW_CODE,0);//leo parte baja del contador de bit 
    reg_file_out = reg_file_read();
    *bit_count_im |= ((uint64_t) reg_file_out);

    /////////////////////////////contador de errores real/////////////////////////
    reg_file_write(COUNT_LOG_OP_TYPE,ERROR_COUNT_RE_HIGH_CODE,0);//leo parte alta del contador de bit 
    reg_file_out = reg_file_read();
    *bit_error_re |= ((uint64_t) reg_file_out) << 32;
    reg_file_write(COUNT_LOG_OP_TYPE,ERROR_COUNT_RE_LOW_CODE,0);//leo parte baja del contador de bit 
    reg_file_out = reg_file_read();
    *bit_error_re |= ((uint64_t) reg_file_out);

    /////////////////////////////contador de errores imag/////////////////////////
    reg_file_write(COUNT_LOG_OP_TYPE,ERROR_COUNT_IM_HIGH_CODE,0);//leo parte alta del contador de bit 
    reg_file_out = reg_file_read();
    *bit_error_im |= ((uint64_t) reg_file_out) << 32;
    reg_file_write(COUNT_LOG_OP_TYPE,ERROR_COUNT_IM_LOW_CODE,0);//leo parte baja del contador de bit 
    reg_file_out = reg_file_read();
    *bit_error_im |= ((uint64_t) reg_file_out);

    return;
}
void soft_delay(int delay){
    for(int i=0; i<delay; i++){}
    return;    
}
void wait_mem_done(){
    reg_file_write(MEM_OP_TYPE, MEM_DONE_CODE, 0);
    while(!reg_file_read())
        reg_file_write(MEM_OP_TYPE, MEM_DONE_CODE, 0);
    return;
}

void get_1k_data_from_mem(uint32_t * buff, uint16_t init_address){
    reg_file_write(MEM_OP_TYPE, READ_ENABLE_CODE , 1);
    for( int i=init_address; i < (init_address + 1024); i++ ){
        reg_file_write(MEM_OP_TYPE, READ_ADDR_CODE , i); //escribo la direccion que quiero leer
        reg_file_write(MEM_OP_TYPE, READ_DATA_CODE , 0); //leo el dato
        buff[i] = reg_file_read();
    }
    reg_file_write(MEM_OP_TYPE, READ_ENABLE_CODE ,0);
    return;
}
