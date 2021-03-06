#include <stdio.h>
#include <string.h>
#include "xparameters.h"
#include "xil_cache.h"
#include "xgpio.h"
#include "platform.h"
#include "microblaze_sleep.h"
#include "uart_manager/uart_manager.h"
#include "reg_file_manager/reg_file_manager.h"

#define PORT_IN	 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID
#define PORT_OUT 		XPAR_AXI_GPIO_0_DEVICE_ID //XPAR_GPIO_0_DEVICE_ID

//Device_ID Operaciones
#define def_SOFT_RST            0
#define def_ENABLE_MODULES      1
#define def_LOG_RUN             2
#define def_LOG_READ            3


/*
XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;
u32 GPO_Value;
u32 GPO_Param;
*/
#define BUFF_LEN 1024
#define DATA_NBYTES 4

#define RESET 0x00
#define ENB_TX 0x01
#define ENB_RX 0x02
#define ENB_BER 0x03
#define ENB_ALL 0x04
#define DISABLE_TX 0x05
#define DISABLE_RX 0x06
#define DISABLE_BER 0x07
#define DISABLE_ALL 0x08
#define SET_PHASE 0x09
#define READ_BER 0x0a
#define LOG 0x0b

int main()
{
	init_platform();
	int Status;

    reg_file_init();
    uart_init();

    u32 reg_file_out;
    u32 enable_reg;
    enable_reg = 0;

    //////variables de estado de register file////////////
 
    /////////////////////////////////////////////////////
    unsigned char device = 255;
    unsigned char data[BUFF_LEN];

    uint64_t *bit_error_re;
    bit_error_re = &data[0];
    uint64_t *bit_count_re;
    bit_count_re = &data[8];
    uint64_t *bit_error_im;
    bit_error_im = &data[16];
    uint64_t *bit_count_im;
    bit_count_im = &data[24];

    char * ack;

    while(1){
        
    	uart_receive(data, &device);
    	///////////////////////////////////////////////////////
    	//realizar checkeo de error de la funcion uart_receive
    	///////////////////////////////////////////////////////


    	///////////////////////////////////////////////////////
    	//realizar echo
    	//////////////////////////////////////////////////////

    	switch((uint8_t) device){
    		case RESET:
    			reg_file_write(REG_OP_TYPE, RESET_CODE, 0); //pongo el reset
    			soft_delay(10);
    			reg_file_write(REG_OP_TYPE, RESET_CODE, 1); // saco el reset
                ack = "ACK: System Reset";
                uart_send(ack, 18, 0);
				break;
			case ENB_TX:
				enable_reg |= ENABLE_TX;
				reg_file_write(REG_OP_TYPE, ENABLE_CODE, enable_reg);
                ack = "ACK: Enable Tx";
                uart_send(ack, 14, 0);
                break;
			case ENB_RX:
				enable_reg |= ENABLE_RX;
				reg_file_write(REG_OP_TYPE, ENABLE_CODE, enable_reg);
                ack = "ACK: Enable Rx";
                uart_send(ack, 14, 0);
				break;
			case ENB_BER:
				enable_reg |= ENABLE_BER;
				reg_file_write(REG_OP_TYPE, ENABLE_CODE, enable_reg);
                ack = "ACK: Enable BER";
                uart_send(ack, 15, 0);
				break;
			case ENB_ALL:
				enable_reg |= ENABLE_TX | ENABLE_RX | ENABLE_BER;
				reg_file_write(REG_OP_TYPE, ENABLE_CODE, enable_reg);
                ack = "ACK: Enable ALL";
                uart_send(ack, 15, 0);
				break;
			case DISABLE_TX:
				enable_reg &= (~ENABLE_TX);
				reg_file_write(REG_OP_TYPE, ENABLE_CODE, enable_reg);
                ack = "ACK: Disable Tx";
                uart_send(ack, 15, 0);
				break;
			case DISABLE_RX:
				enable_reg &= (~ENABLE_RX);
				reg_file_write(REG_OP_TYPE, ENABLE_CODE, enable_reg);
                ack = "ACK: Disable Rx";
                uart_send(ack, 15, 0);
				break;
			case DISABLE_BER:
				enable_reg &= (~ENABLE_BER);
				reg_file_write(REG_OP_TYPE, ENABLE_CODE, enable_reg);
                ack = "ACK: Disable BER";
                uart_send(ack, 16, 0);
				break;
			case DISABLE_ALL:
				enable_reg &= (~(ENABLE_TX | ENABLE_RX | ENABLE_BER));
				reg_file_write(REG_OP_TYPE, ENABLE_CODE, enable_reg);
                ack = "ACK: Disable ALL";
                uart_send(ack, 16, 0);
				break;
            case SET_PHASE:
                reg_file_write(REG_OP_TYPE, PHASE_CODE, data[0]);
                ack = "ACK: Set Phase to ";
                ack[18] = data[0]+48;
                uart_send(ack, 19, 0);
                break;
			case READ_BER : 
				read_ber_counter(bit_error_re, bit_count_re, bit_error_im, bit_count_im);
                uart_send(data, 32, 0);
				break;
			case LOG :

				// habilitar el o_run del rf
				reg_file_write(MEM_OP_TYPE, RUN_CODE, 1);
				// esperar done
				wait_mem_done();
				reg_file_write(MEM_OP_TYPE, RUN_CODE, 0);
                //leo la posicion de memoria 1
				get_1k_data_from_mem(data, 0);
				uart_send(data, (BUFF_LEN*DATA_NBYTES ), 0);
                
                /*
                reg_file_write(MEM_OP_TYPE, READ_ENABLE_CODE , 1);
                reg_file_write(MEM_OP_TYPE, READ_ADDR_CODE , 0);
                reg_file_write(MEM_OP_TYPE, READ_DATA_CODE , 0);
                u32 caca =  reg_file_read();
                //reg_file_write(MEM_OP_TYPE, READ_ENABLE_CODE ,0);
                uart_send(&caca, 4, 0);
                reg_file_write(MEM_OP_TYPE, READ_ENABLE_CODE ,0);
                */
                


                /*leo 1k datos empezando desde la direccion 0 (segundo argumento de la funcion get_1k)
				get_1k_data_from_mem(data, 0);*/
				//uart_send(data, (BUFF_LEN*DATA_NBYTES ), 0);
				break;
			default :
				break;		
    	}
    }
	cleanup_platform();
	return 0;
}
