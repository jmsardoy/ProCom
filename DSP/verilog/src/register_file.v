`define GPIO_LEN 32
`define OPCODE_LEN 8
`define OP_TYPE_LEN 2

module register_file(
        clk,
        rst,
        gpio_in,
        gpio_out,

        error_count_r,
        error_count_i,
        bit_count_r,
        bit_count_i,

        reset_reg,
        enable_reg,
        phase_reg
    );

    ///////////////////////////////////////////////////////
    // PARAMETERS
    ///////////////////////////////////////////////////////
    parameter GPIO_LEN = `GPIO_LEN;
    parameter OPCODE_LEN = `OPCODE_LEN;
    parameter OP_TYPE_LEN = `OP_TYPE_LEN;

    localparam DATA_LEN = GPIO_LEN-OPCODE_LEN-1;

    localparam ENABLE_LEN = 3;
    localparam PHASE_LEN = 2;
    localparam LOG_COUNT_LEN = 64;


    ///////////////////////////////////////////////////////
    // OPERATIONS
    ///////////////////////////////////////////////////////

    //OPERATION TYPES
    localparam REG_OP_TYPE = 'b00;
    localparam COUNT_LOG_OP_TYPE = 'b10;
    localparam MEM_LOG_OP_TYPE = 'b11;

    //CODE TYPES
    //---SET_REG_OP_TYPE
    localparam RESET_CODE  = 'h0;
    localparam ENABLE_CODE = 'h1;
    localparam PHASE_CODE  = 'h2;
    //---COUNT_LOG_OP_TYPE
    localparam BIT_COUNT_RE_HIGH_CODE   = 'h00;
    localparam BIT_COUNT_RE_LOW_CODE    = 'h01;
    localparam BIT_COUNT_IM_HIGH_CODE   = 'h02;
    localparam BIT_COUNT_IM_LOW_CODE    = 'h03;
    localparam ERROR_COUNT_RE_HIGH_CODE = 'h04;
    localparam ERROR_COUNT_RE_LOW_CODE  = 'h05;
    localparam ERROR_COUNT_IM_HIGH_CODE = 'h06;
    localparam ERROR_COUNT_IM_LOW_CODE  = 'h07;
    localparam LATCH_COUNTS_CODE        = 'h08;
    //---MEM_LOG_OP_TYPE
    ///////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////
    // MICROBLAZE PORTS
    ///////////////////////////////////////////////////////
    input wire clk;
    input wire rst;

    input wire  [GPIO_LEN - 1 : 0] gpio_in;
    output reg  [GPIO_LEN - 1 : 0] gpio_out;
    ///////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////
    // REGISTERS PORTS
    ///////////////////////////////////////////////////////
    input wire [LOG_COUNT_LEN - 1 : 0] error_count_r;
    input wire [LOG_COUNT_LEN - 1 : 0] error_count_i;
    input wire [LOG_COUNT_LEN - 1 : 0] bit_count_r;
    input wire [LOG_COUNT_LEN - 1 : 0] bit_count_i;
    output reg                         reset_reg;
    output reg [ENABLE_LEN - 1 : 0]    enable_reg; //[ber, rx, tx]
    output reg [PHASE_LEN - 1 : 0]     phase_reg;

    reg [LOG_COUNT_LEN - 1 : 0] error_count_r_reg;
    reg [LOG_COUNT_LEN - 1 : 0] error_count_i_reg;
    reg [LOG_COUNT_LEN - 1 : 0] bit_count_r_reg;
    reg [LOG_COUNT_LEN - 1 : 0] bit_count_i_reg;
    ///////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////
    // INTERNAL SIGNALS
    ///////////////////////////////////////////////////////

    wire [OPCODE_LEN - 1 : 0]               opcode  = gpio_in[GPIO_LEN - 1 -: OPCODE_LEN];
    wire                                    enable  = gpio_in[GPIO_LEN - 1 - OPCODE_LEN];
    wire [DATA_LEN - 1 : 0]                 data    = gpio_in[DATA_LEN - 1 : 0];
    wire [OP_TYPE_LEN - 1 : 0]              op_type = opcode[OPCODE_LEN - 1 -: OP_TYPE_LEN];
    wire [OPCODE_LEN - OP_TYPE_LEN - 1 : 0] code    = opcode[OPCODE_LEN - OP_TYPE_LEN - 1 : 0];
    ///////////////////////////////////////////////////////



    always@(posedge clk or negedge rst)
    begin
        if (!rst) begin
            reset_reg <= 0;
            enable_reg <= {ENABLE_LEN{1'b0}};
            phase_reg <= 0;

            gpio_out <= 1;
            bit_count_r_reg <= 0;
            bit_count_i_reg <= 0;
            error_count_r_reg <= 0;
            error_count_i_reg <= 0;
        end
        else begin
            if (enable) begin
                case (op_type)
                    REG_OP_TYPE: begin
                        case (code)
                            RESET_CODE: reset_reg <= data[0];
                            ENABLE_CODE: enable_reg <= data[ENABLE_LEN -1 : 0];
                            PHASE_CODE: phase_reg <= data[PHASE_LEN - 1: 0];
                        endcase

                    end
                    COUNT_LOG_OP_TYPE: begin
                        case (code)
                            BIT_COUNT_RE_HIGH_CODE   : gpio_out <= bit_count_r_reg[LOG_COUNT_LEN - 1 : LOG_COUNT_LEN/2];
                            BIT_COUNT_RE_LOW_CODE    : gpio_out <= bit_count_r_reg[LOG_COUNT_LEN/2 - 1 : 0];
                            BIT_COUNT_IM_HIGH_CODE   : gpio_out <= bit_count_i_reg[LOG_COUNT_LEN - 1 : LOG_COUNT_LEN/2];
                            BIT_COUNT_IM_LOW_CODE    : gpio_out <= bit_count_i_reg[LOG_COUNT_LEN/2 - 1 : 0];
                            ERROR_COUNT_RE_HIGH_CODE : gpio_out <= error_count_r_reg[LOG_COUNT_LEN - 1 : LOG_COUNT_LEN/2];
                            ERROR_COUNT_RE_LOW_CODE  : gpio_out <= error_count_r_reg[LOG_COUNT_LEN/2 - 1 : 0];
                            ERROR_COUNT_IM_HIGH_CODE : gpio_out <= error_count_i_reg[LOG_COUNT_LEN - 1 : LOG_COUNT_LEN/2];
                            ERROR_COUNT_IM_LOW_CODE  : gpio_out <= error_count_i_reg[LOG_COUNT_LEN/2 - 1 : 0];
                            LATCH_COUNTS_CODE: begin
                                bit_count_r_reg <= bit_count_r;
                                bit_count_i_reg <= bit_count_i;
                                error_count_r_reg <= error_count_r;
                                error_count_i_reg <= error_count_i;
                            end
                        endcase
                    end
                    /*
                    MEM_LOG_OP_TYPE: begin

                    end
                    */
                    
                endcase
            end
        end
    end

endmodule
