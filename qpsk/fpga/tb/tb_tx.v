`timescale 1ns/100ps

`define SEED 9'h1AA

module tb_tx();
    reg rst;
    reg clk;
    reg clk_prbs;
    wire bit_out;
    wire [8:0] tb_tx_out;

    localparam COEF = {8'h0, 8'hfe, 8'hff, 8'h0, 8'h2, 8'h0, 8'hfb, 8'hf5,
                        8'hf9, 8'ha, 8'h25, 8'h3e, 8'h48, 8'h3e, 8'h25, 8'ha, 
                        8'hf9, 8'hf5,8'hfb, 8'h0, 8'h2, 8'h0, 8'hff, 8'hfe};

    initial begin
        rst = 0;
        clk = 1;
        clk_prbs = 1;
        #8 rst = 1;
    end

    always #1 clk = ~clk;
    always #4 clk_prbs = ~clk_prbs;

    prbs
        #(
        .SEED (`SEED)
        )
    prbs_r(
        .clk (clk_prbs),
        .rst (rst),
        .bit_out (bit_out)
        );

    tx
        #(
        .COEF(COEF)
        )
    tx_r(
        .clk (clk),
        .rst (rst),
        .tx_in (bit_out),
        .tx_out (tb_tx_out)
        );
endmodule
