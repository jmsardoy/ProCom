`timescale 1ns/100ps

`define SEED_R 9'h1AA
`define SEED_I 9'h1FE
`define UPSAMPLE 4
`define REG_COUNT_LEN 64

module dsp(
           rst,
           clk,
           i_enable_tx,
           i_enable_rx,
           i_enable_ber,
           i_phase,
           o_error_count_r,
           o_error_count_i,
           o_bit_count_r,
           o_bit_count_i,
           o_led
           );
    
    parameter SEED_R = `SEED_R;
    parameter SEED_I = `SEED_I;

    localparam REG_COUNT_LEN = `REG_COUNT_LEN;
    localparam UPSAMPLE = `UPSAMPLE;

    input rst;
    input clk;
    input i_enable_tx;
    input i_enable_rx;
    input i_enable_ber;
    input [1:0] i_phase;

    output [REG_COUNT_LEN - 1 : 0] o_error_count_r;
    output [REG_COUNT_LEN - 1 : 0] o_error_count_i;
    output [REG_COUNT_LEN - 1 : 0] o_bit_count_r;
    output [REG_COUNT_LEN - 1 : 0] o_bit_count_i;
    output [3:0] o_led;

    wire error_flag_r;
    wire prbs_out_r;
    wire [7:0] tx_out_r;
    wire rx_out_r;

    wire error_flag_i;
    wire prbs_out_i;
    wire [7:0] tx_out_i;
    wire rx_out_i;

    reg [1:0] clk_counter;
    reg enable_prbs;
    reg valid_prbs;
    reg valid_ber;
    reg [1:0] phase;
    reg ber_rst;
    reg enable_tx;
    reg enable_rx;


    assign o_led[0] = enable_tx;
    assign o_led[1] = enable_rx;
    assign o_led[2] = 1'b0; 
    assign o_led[3] = ~(error_flag_r | error_flag_i);

    localparam COEF = {8'h0, 8'hfe, 8'hff, 8'h0, 8'h2, 8'h0, 8'hfb, 8'hf5,
                        8'hf9, 8'ha, 8'h25, 8'h3e, 8'h48, 8'h3e, 8'h25, 8'ha, 
                        8'hf9, 8'hf5,8'hfb, 8'h0, 8'h2, 8'h0, 8'hff, 8'hfe};

    always @ (posedge clk or negedge rst) begin
        if (!rst) begin
            clk_counter <= 0;
            valid_prbs <= 0;
            valid_ber <= 0;
            phase <= 0;
            ber_rst <= 0;
            enable_tx <= 0;
            enable_rx <= 0;
        end
        else begin
            clk_counter <= clk_counter+1;
            if (clk_counter == 0) begin
                valid_prbs <= 1;
                valid_ber <= 1;
            end
            else begin
                valid_prbs <= 0;
                valid_ber <= 0;
            end

            phase <= i_phase;
            enable_tx <= i_enable_tx;
            enable_rx <= i_enable_rx;

            if ((i_phase != phase)) begin
                ber_rst <= 0;
            end
            else if ((enable_rx == 0) && (i_enable_rx == 1)) begin
                ber_rst <= 0;
            end
            else begin
                ber_rst <= 1;
            end
         end
    end

    prbs
        #(
        .SEED (SEED_R)
        )
    prbs_r(
        .clk (clk),
        .rst (rst),
        .enable (enable_tx),
        .valid (valid_prbs),
        .bit_out (prbs_out_r)
        );

    tx
        #(
        .COEF(COEF)
        )
    tx_r(
        .clk (clk),
        .rst (rst),
        .enable (enable_tx),
        .tx_in (prbs_out_r),
        .tx_out (tx_out_r)
        );

    rx
        #(
        .COEF(COEF)
        )
    rx_r(
        .clk (clk),
        .rst (rst),
        .enable (enable_rx),
        .rx_in (tx_out_r),
        .phase_in (phase),
        .rx_out (rx_out_r)
        );

    ber
        #(
        .REG_LEN(REG_COUNT_LEN)
        )
    ber_r(
        .clk (clk),
        .rst (ber_rst),
        .enable (i_enable_ber),
        .valid (valid_ber),
        .sx (prbs_out_r),
        .dx (rx_out_r),
        .error_count (o_error_count_r),
        .bit_count (o_bit_count_r),
        .error_flag (error_flag_r)
        );

    prbs
        #(
        .SEED (SEED_I)
        )
    prbs_i(
        .clk (clk),
        .rst (rst),
        .enable (enable_tx),
        .valid (valid_prbs),
        .bit_out (prbs_out_i)
        );

    tx
        #(
        .COEF(COEF)
        )
    tx_i(
        .clk (clk),
        .rst (rst),
        .enable (enable_tx),
        .tx_in (prbs_out_i),
        .tx_out (tx_out_i)
        );

    rx
        #(
        .COEF(COEF)
        )
    rx_i(
        .clk (clk),
        .rst (rst),
        .enable (enable_rx),
        .rx_in (tx_out_i),
        .phase_in (phase),
        .rx_out (rx_out_i)
        );

    ber
        #(
        .REG_LEN(REG_COUNT_LEN)
        )
    ber_i(
        .clk (clk),
        .rst (ber_rst),
        .enable (i_enable_ber),
        .valid (valid_ber),
        .sx (prbs_out_i),
        .dx (rx_out_i),
        .error_count (o_error_count_i),
        .bit_count (o_bit_count_i),
        .error_flag (error_flag_i)
        );

endmodule
