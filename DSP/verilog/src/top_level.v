/*-----------------------------------------------------------------------------
-- Archivo       : top_level.v
-- Organizacion  : Fundacion Fulgor 
-------------------------------------------------------------------------------
-- Descripcion   : Top level de implementacion
-------------------------------------------------------------------------------
-- Autor         : Juan Manuel Sardoy
-------------------------------------------------------------------------------*/

`include "artyc_include.v"


module top_level(
        out_leds_rgb0,
        out_leds_rgb1,
        out_leds_rgb2,
        out_leds_rgb3,
        out_leds,
        out_tx_uart,
        in_rx_uart,
        in_reset,
        i_sw,
        clk100
    );

    ///////////////////////////////////////////
    // Parameter
    ///////////////////////////////////////////
    parameter NB_GPIOS              = `NB_GPIOS;
    parameter NB_LEDS               = `NB_LEDS;
    parameter NB_LEDS_RGB           = `NB_LEDS_RGB;
    parameter NB_SWITCHS            = `NB_SWITCHS;



    ///////////////////////////////////////////
    // Ports
    ///////////////////////////////////////////
    output wire [NB_LEDS - 1 : 0]                     out_leds;
    output [NB_LEDS_RGB - 1 : 0]                      out_leds_rgb0;
    output [NB_LEDS_RGB - 1 : 0]                      out_leds_rgb1;
    output [NB_LEDS_RGB - 1 : 0]                      out_leds_rgb2;
    output [NB_LEDS_RGB - 1 : 0]                      out_leds_rgb3;

    output wire                                       out_tx_uart;
    input wire                                        in_rx_uart;
    input wire                                        in_reset;
    input wire [NB_SWITCHS - 1 : 0]                   i_sw;
    input                                             clk100;

    ///////////////////////////////////////////
    // Vars
    ///////////////////////////////////////////
    wire [NB_GPIOS - 1 : 0]                           gpo0;
    wire [NB_GPIOS - 1 : 0]                           gpi0;

    wire                                              locked;

    wire                                              soft_reset;
    wire                                              clockdsp;


    wire reset_dsp;
    wire [2 : 0] enable_dsp;
    wire [1 : 0] phase_dsp;
    wire [63 : 0] error_count_r; 
    wire [63 : 0] error_count_i; 
    wire [63 : 0] bit_count_r; 
    wire [63 : 0] bit_count_i; 


    ///////////////////////////////////////////
    // MicroBlaze
    ///////////////////////////////////////////
    MicroGPIO u_micro(
        .clock100         (clockdsp    ),  // Clock aplicacion
        .gpio_rtl_tri_o   (gpo0        ),  // GPIO
        .gpio_rtl_tri_i   (gpi0        ),  // GPIO
        .reset            (in_reset    ),  // Hard Reset
        .sys_clock        (clk100      ),  // Clock de FPGA
        .o_lock_clock     (locked      ),  // Senal Lock Clock
        .usb_uart_rxd     (in_rx_uart  ),  // UART
        .usb_uart_txd     (out_tx_uart )   // UART
    );
    
    register_file u_reg_file (
        .rst (in_reset),
        .clk (clockdsp),
        .gpio_in (gpo0),
        .gpio_out (gpi0),

        .error_count_r (error_count_r),
        .error_count_i (error_count_i),
        .bit_count_r (bit_count_r),
        .bit_count_i (bit_count_i),

        .reset_reg (reset_dsp),
        .enable_reg (enable_dsp),
        .phase_reg (phase_dsp)
    );

    dsp u_dsp(
        .rst (reset_dsp),
        .clk (clockdsp),
        .i_enable_tx (enable_dsp[0]),
        .i_enable_rx (enable_dsp[1]),
        .i_enable_ber (enable_dsp[2]),
        .i_phase (phase_dsp),
        .o_error_count_r (error_count_r),
        .o_error_count_i (error_count_i),
        .o_bit_count_r (bit_count_r),
        .o_bit_count_i (bit_count_i),
        .o_led (out_leds)
    );



    ///////////////////////////////////////////
    // Leds
    ///////////////////////////////////////////
    /*
    assign out_leds[0] = locked;
    assign out_leds[1] = ~in_reset;
    assign out_leds[2] = gpo0[12];
    assign out_leds[3] = gpo0[13];
    */

    /*
    assign out_leds_rgb0[0] = gpo0[0];
    assign out_leds_rgb0[1] = gpo0[1];
    assign out_leds_rgb0[2] = gpo0[2];

    assign out_leds_rgb1[0] = gpo0[3];
    assign out_leds_rgb1[1] = gpo0[4];
    assign out_leds_rgb1[2] = gpo0[5];
    */
    assign out_leds_rgb0[0] = reset_dsp;
    assign out_leds_rgb0[1] = 0;
    assign out_leds_rgb0[2] = 0;

    assign out_leds_rgb1[0] = enable_dsp[0];
    assign out_leds_rgb1[1] = 0;
    assign out_leds_rgb1[2] = 0;

    assign out_leds_rgb2[0] = enable_dsp[1];
    assign out_leds_rgb2[1] = 0;
    assign out_leds_rgb2[2] = 0;

    assign out_leds_rgb3[0] = gpo0[9];
    assign out_leds_rgb3[1] = 0;
    assign out_leds_rgb3[2] = 0;

    assign gpi0[3  : 0] = i_sw;
    assign gpi0[31 : 4] = {28{1'b0}};
    ///////////////////////////////////////////
    // Register File
    ///////////////////////////////////////////

    //.out_rf_to_micro_data  (gpi0),

endmodule
