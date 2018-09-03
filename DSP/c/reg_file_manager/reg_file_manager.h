#include "xgpio.h"
#include <stdio.h>

//OP_TYPES DEFINES
#define REG_OP_TYPE 0
#define COUNT_LOG_OP_TYPE 2
#define MEM_OP_TYPE 3

//REG_OP CODES DEFINES
#define RESET_CODE 0
#define ENABLE_CODE 1
#define PHASE_CODE 2

//ENABLE_CODE DATAS
#define ENABLE_TX  1
#define ENABLE_RX  2
#define ENABLE_BER 4
 //LOG_MEM_OP
#define SET_RUN_LOG_CODE 3
#define SET_READ_LOG_CODE 4
#define ADDR_MEM_CODE 5
#define READ_MEM_DONE_CODE 6
//COUN_LOG_OP CODES DEFINES
#define BIT_COUNT_RE_HIGH_CODE    0
#define BIT_COUNT_RE_LOW_CODE     1
#define BIT_COUNT_IM_HIGH_CODE    2
#define BIT_COUNT_IM_LOW_CODE     3
#define ERROR_COUNT_RE_HIGH_CODE  4
#define ERROR_COUNT_RE_LOW_CODE   5
#define ERROR_COUNT_IM_HIGH_CODE  6
#define ERROR_COUNT_IM_LOW_CODE   7
#define BER_LATCH_CODE      	  8



XGpio GpioOutput;
XGpio GpioParameter;
XGpio GpioInput;

void reg_file_init(void);
void reg_file_write(u32, u32, u32);
u32 reg_file_read(void);
void read_ber_counter(uint64_t *, uint64_t *, uint64_t *, uint64_t *);
void wait_mem_done (void);
void get_1kb_data_from_mem( uint32_t * , uint16_t  );  
void soft_delay(int);
