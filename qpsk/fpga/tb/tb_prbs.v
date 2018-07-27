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
   /*
   ledsOn
     #(
       .N_LEDS   (N_LEDS)  ,
       .NB_SEL   (NB_SEL)  ,
       .NB_SW    (NB_SW)
       )
   u_shiftleds
     (
      .o_led     (o_led)    ,
      .o_led_b   (o_led_b)  ,
      .o_led_g   (o_led_g)  ,
      .o_led_r   (o_led_r)  ,
      .i_sw      (i_sw)     ,
      .i_btn     (i_btn)    ,
      .ck_rst    (ck_rst)   ,
      .CLK100MHZ (CLK100MHZ)
      );
      */
endmodule

    
