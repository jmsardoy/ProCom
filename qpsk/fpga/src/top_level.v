`timescale 1ns/100ps

`define SEED_R 9'h1AA
`define UPSAMPLE 4

module top_level(
            rst,
            CLK100MHZ,
            i_sw,
            o_led
            );
    
    parameter SEED_R = `SEED_R;
    localparam UPSAMPLE = `UPSAMPLE;

    input rst;
    input CLK100MHZ;
    input [3:0] i_sw;

    output [3:0] o_led;

    wire clk;
    wire enable_tx;
    wire error_flag;
    wire prbs_out_r;
    wire [7:0] tx_out_r;
    wire rx_out_r;
    reg [1:0] clk_counter;
    reg enable_prbs;
    reg enable_ber;
    reg [1:0] phase;
    reg ber_rst;
    reg enable_rx;

    assign clk = CLK100MHZ;
    assign enable_tx = i_sw[0];
    //assign enable_rx = i_sw[1];

    assign o_led[0] = enable_tx;
    assign o_led[1] = enable_rx;
    assign o_led[2] = 1'b0; 
    assign o_led[3] = ~error_flag;

    localparam COEF = {8'h0, 8'hfe, 8'hff, 8'h0, 8'h2, 8'h0, 8'hfb, 8'hf5,
                        8'hf9, 8'ha, 8'h25, 8'h3e, 8'h48, 8'h3e, 8'h25, 8'ha, 
                        8'hf9, 8'hf5,8'hfb, 8'h0, 8'h2, 8'h0, 8'hff, 8'hfe};

    always @ (posedge clk or negedge rst) begin
        if (!rst) begin
            clk_counter <= 0;
            enable_prbs <= 0;
            enable_ber <= 0;
            phase <= 0;
            ber_rst <= 0;
            enable_rx <= 0;
        end
        else begin
            clk_counter <= clk_counter+1;
            if (clk_counter == 0) begin
                enable_prbs <= 1;
                enable_ber <= 1;
            end
            else begin
                enable_prbs <= 0;
                enable_ber <= 0;
            end

            phase <= i_sw[3:2];
            enable_rx <= i_sw[1];
            if ((i_sw[3:2] != phase)) begin
                ber_rst <= 0;
            end
            else if (enable_rx == 0) begin
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
        .enable (enable_prbs),
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
    ber_r(
        .clk (clk),
        .rst (ber_rst),
        .enable (enable_ber),
        .sx (prbs_out_r),
        .dx (rx_out_r),
        .error_flag (error_flag)
        );

endmodule
