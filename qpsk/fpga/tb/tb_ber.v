`timescale 1ns/100ps

`define SEED 9'h1AA

module tb_ber();
    reg rst;
    reg clk;
    reg enable_prbs;
    reg enable_tx;
    reg enable_rx;
    reg enable_ber;
    reg [1:0] phase;
    wire bit_out;
    wire [7:0] tb_tx_out;
    wire tb_rx_out;
    wire error_flag;
    reg [1:0] clk_counter;
    reg [31:0] clk_index;

    localparam COEF = {8'h0, 8'hfe, 8'hff, 8'h0, 8'h2, 8'h0, 8'hfb, 8'hf5,
                        8'hf9, 8'ha, 8'h25, 8'h3e, 8'h48, 8'h3e, 8'h25, 8'ha, 
                        8'hf9, 8'hf5,8'hfb, 8'h0, 8'h2, 8'h0, 8'hff, 8'hfe};

    initial begin
        rst = 0;
        clk = 0;
        enable_prbs = 0;
        enable_tx = 1;
        enable_rx = 1;
        enable_ber = 0;
        clk_counter = 0;
        clk_index = 0;
        phase = 1;
        #2 rst = 1;
    end

    always #1 clk = ~clk;

    always @ (posedge clk or negedge rst) begin
        if (~rst)
            clk_index <= 0;
        else
            clk_index <= clk_index+1;
    end
    //always #4 clk_prbs = ~clk_prbs;
    always @ (posedge clk or negedge rst) begin
        if (~rst) 
            clk_counter <= 0;
        else
            clk_counter <= clk_counter+1;
            if ((clk_counter)%4 == 1) begin
                enable_prbs <= 1;
                enable_ber <= 1;
            end
            else begin
                enable_prbs <= 0;
                enable_ber <= 0;
            end
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

    rx
        #(
        .COEF(COEF)
        )
    rx_r(
        .clk (clk),
        .rst (rst),
        .enable (enable_rx),
        .rx_in (tb_tx_out),
        .phase_in (phase),
        .rx_out (tb_rx_out)
        );

    ber
    ber_r(
        .clk (clk),
        .rst (rst),
        .enable (enable_ber),
        .sx (bit_out),
        .dx (tb_rx_out),
        .error_flag (error_flag)
        );

endmodule
