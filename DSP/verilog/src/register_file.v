`define GPIO_LEN 32
`define OPCODE_LEN 8

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

    localparam DATA_LEN = GPIO_LEN-OPCODE_LEN-1;

    localparam ENABLE_LEN = 3;
    localparam PHASE_LEN = 2;
    localparam LOG_COUNT_LEN = 64;

    localparam RESET_OP = 0'h00;
    localparam ENABLE_OP = 0'h01;
    localparam PHASE_OP = 0'h02;
    ///////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////
    // MICROBLAZE PORTS
    ///////////////////////////////////////////////////////
    input wire clk;
    input wire rst;
    input wire [GPIO_LEN - 1 : 0] gpio_in;

    output wire [GPIO_LEN - 1 : 0] gpio_out;
    ///////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////
    // REGISTERS PORTS
    ///////////////////////////////////////////////////////
    input wire [LOG_COUNT_LEN - 1 : 0] error_count_r;
    input wire [LOG_COUNT_LEN - 1 : 0] error_count_i;
    input wire [LOG_COUNT_LEN - 1 : 0] bit_count_r;
    input wire [LOG_COUNT_LEN - 1 : 0] bit_count_i;
    output reg reset_reg;
    output reg [ENABLE_LEN - 1 : 0] enable_reg; //[ber, rx, tx]
    output reg [PHASE_LEN - 1 : 0] phase_reg;
    ///////////////////////////////////////////////////////

    ///////////////////////////////////////////////////////
    // INTERNAL SIGNALS
    ///////////////////////////////////////////////////////
    wire reset = ~rst;
    wire [OPCODE_LEN - 1 : 0] opcode = gpio_in[GPIO_LEN - 1 -: OPCODE_LEN];
    wire enable = gpio_in[GPIO_LEN - 1 - OPCODE_LEN];
    wire [DATA_LEN - 1 : 0] data = gpio_in[DATA_LEN - 1 : 0];
    ///////////////////////////////////////////////////////



    always@(posedge clk)
    begin
        if (reset) begin
            reset_reg <= 0;
            enable_reg <= {ENABLE_LEN{1'b0}};
            phase_reg <= 0;
        end
        else begin
            if (enable) begin
                case(opcode)
                   RESET_OP: reset_reg <= data[0];
                   ENABLE_OP: enable_reg <= data[ENABLE_LEN - 1 : 0];
                   PHASE_OP: phase_reg <= data[PHASE_LEN - 1 : 0];
                endcase
            end
        end
    end

endmodule
