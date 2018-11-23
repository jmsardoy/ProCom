`timescale 1ns/100ps

`define SEED 9'h1AA

module tb_mem_log();


    reg clk;
    reg rst;
    reg i_run;
    reg i_read;
    reg [2 : 0] i_address;
    reg [31 : 0] i_data;
    wire o_mem_full;
    wire [31 : 0] o_data;
    reg [31: 0] state;

    initial begin
        rst = 0;
        clk = 1;
        i_run = 0;
        i_read = 0;
        i_address = 0;
        i_data = 0;
        state = 0;

        /*
        #1 rst = 1;
        #3 i_run = 1;
        #5 i_run = 0;
        #16 i_run = 1;
        #18 i_read = 1;
        #4 i_address = 0;
        #2 i_address = 1;
        #2 i_address = 2;
        #2 i_address = 3;
        #2 i_address = 4;
        #2 i_address = 5;
        #2 i_address = 6;
        #2 i_address = 7;
        */
    end

    always #1 clk = ~clk;

    always #2 i_data = i_data+1;

    always@(posedge clk) begin
        case (state)
            1: rst <= 1;
            2: i_run <= 1;
            3: i_run <= 0;
            15: i_run <= 1;
            16: i_run <= 0;
            30: i_read <= 1;
        endcase
        if (state>30) i_address <= i_address+1;
        
        state <= state+1;
    end

    mem_log
    #(
        .RAM_WIDTH(32),
        .RAM_ADDR_NBIT(3)
    )
    mem_log_u(
        .clk (clk),
        .rst (rst),
        .i_run(i_run),
        .i_read(i_read),
        .i_address(i_address),
        .i_data(i_data),
        .o_mem_full(o_mem_full),
        .o_data(o_data)
        );
endmodule

    
