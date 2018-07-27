`timescale 1ns/100ps

`define SEED 9'h1AA

module tb_tx();
    reg rst;
    reg clk;
    reg clk_prbs;
    reg enable_prbs;
    reg enable_tx;
    reg [1:0] clk_counter;
    wire bit_out;
    wire [8:0] tb_tx_out;

    localparam COEF = {8'h0, 8'hfe, 8'hff, 8'h0, 8'h2, 8'h0, 8'hfb, 8'hf5,
                        8'hf9, 8'ha, 8'h25, 8'h3e, 8'h48, 8'h3e, 8'h25, 8'ha, 
                        8'hf9, 8'hf5,8'hfb, 8'h0, 8'h2, 8'h0, 8'hff, 8'hfe};

    initial begin
        rst = 0;
        clk = 1;
        enable_prbs = 0;
        enable_tx = 1;
        clk_counter = 0;
        #8 rst = 1;
    end

    always #1 clk = ~clk;
    always @ (posedge clk) begin
        clk_counter = clk_counter+1;
        if (clk_counter == 0)
            enable_prbs <= 1;
        else
            enable_prbs <= 0;
    end

    prbs
        #(
        .SEED (`SEED)
        )
    prbs_r(
        .clk (clk),
        .rst (rst),
        .enable (enable_prbs),
        .bit_out (bit_out)
        );

    tx
        #(
        .COEF(COEF)
        )
    tx_r(
        .clk (clk),
        .rst (rst),
        .enable (enable_tx),
        .tx_in (bit_out),
        .tx_out (tb_tx_out)
        );
endmodule
