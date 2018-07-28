`timescale 1ns/100ps

`define SEED 9'h1AA

module tb_prbs();

    reg rst;
    wire bit_out;
    reg clk;
    reg enable;

    initial begin
        rst = 0;
        clk = 0;
        enable = 1;
        #1 rst = 1;
        #1022 rst = 0;
        #100 rst = 1;
    end

    always #1 clk = ~clk;

    prbs
        #(
        .SEED (`SEED)
        )
    prbs_r(
        .clk (clk),
        .rst (rst),
        .enable (enable),
        .bit_out (bit_out)
        );
endmodule

    
