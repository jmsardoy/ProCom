`timescale 1ns / 1ps

`define N_LEDS 4
`define NB_SEL 2
`define NB_COUNT 32
`define NB_SW 4
`define NB_BTN 4
`define NB_COUNTER 32

module leds_srfs( 
                 o_led  ,
                 o_led_r,
                 o_led_g,
                 o_led_b,
                 i_sw   ,
                 i_btn  ,
                 ck_rst ,
                 CLK100MHZ
                );

    // Parameters
    parameter N_LEDS = `N_LEDS;
    parameter NB_SEL = `NB_SEL;
    parameter NB_SW  = `NB_SW;
    parameter NB_BTN  = `NB_BTN;
    
    

    // Localparam
    localparam NB_COUNTER = `NB_COUNTER;
    localparam COLOR_SEL0 = 3'b001;
    localparam COLOR_SEL1 = 3'b010;
    localparam COLOR_SEL2 = 3'b100;
    localparam SEL_R0 = `NB_SEL'h0;
    localparam SEL_R1 = `NB_SEL'h1;
    localparam SEL_R2 = `NB_SEL'h2;
    localparam SEL_R3 = `NB_SEL'h3;
    localparam R0 = 2 ** (`NB_COUNTER - 10);
    localparam R1 = 2 ** (`NB_COUNTER - 9);
    localparam R2 = 2 ** (`NB_COUNTER - 8);
    localparam R3 = 2 ** (`NB_COUNTER - 7);
    // Ports
    output [N_LEDS - 1 : 0] o_led;
    output [N_LEDS - 1 : 0] o_led_r;
    output [N_LEDS - 1 : 0] o_led_g;
    output [N_LEDS - 1 : 0] o_led_b;

    input [NB_SW   - 1 : 0] i_sw;
    input [NB_BTN  - 1 : 0] i_btn;
    input                   CLK100MHZ;
    input                   ck_rst;

    // Vars
    wire                    reset;
    wire [N_LEDS*3 - 1 : 0] ledsRGB;
    wire [NB_COUNTER-1 : 0] compare_value;
    wire                    compare_signal;
    reg  [N_LEDS   - 1 : 0] load_led;
    reg  [NB_COUNTER-1 : 0] counter;
    reg  [N_LEDS - 1   : 0] shift_reg;
    reg  [N_LEDS - 1   : 0] flash;
    reg  [N_LEDS - 1   : 0] o_srfs;
    reg                     srfs_flag;
    reg  [2            : 0] color_sel;
    reg  [NB_BTN  - 1  : 0] btn_prev_state;


    assign reset     =  ~ck_rst;
    
    //Compare MUX
    assign compare_value = (i_sw[2:1] == SEL_R0) ? R0 :
                           (i_sw[2:1] == SEL_R1) ? R1 :
                           (i_sw[2:1] == SEL_R2) ? R2 :
                                                   R3 ;                           

    //Compare Block
    assign compare_signal = (counter == compare_value) ? 1'b1 : 1'b0;


    //Counter
    always@(posedge CLK100MHZ or posedge reset) begin
        if(reset) begin
            counter <= 0;
        end
        else if (i_sw[0]) begin
            counter <= counter + 1;
            if (counter >= compare_value) begin
                counter <= 0;
            end
        end
        else begin
            counter <= counter;
        end
    end

    //ShiftReg
    always@(posedge CLK100MHZ or posedge reset) begin
        if(reset) begin
            shift_reg <= {{(N_LEDS-1){1'b0}}, 1'b1};
        end
        else if(compare_signal) begin
            if(i_sw[3])
                shift_reg <= {shift_reg[N_LEDS-2:0], shift_reg[N_LEDS-1]};
            else
                shift_reg <= {shift_reg[0], shift_reg[N_LEDS-1:1]};
        end
        else begin
            shift_reg <= shift_reg;
        end
    end
    
    //Flash
    always@(posedge CLK100MHZ or posedge reset) begin
        if(reset)
            flash <= {N_LEDS{1'b1}};
        else if(compare_signal)
            flash <= ~flash;
        else
            flash <= flash;
    end

    //Button logic
    always@(posedge CLK100MHZ or posedge reset) begin
        if (reset) begin
            srfs_flag <= 1'b0;
            color_sel <= 3'b001;
            btn_prev_state <= 4'b0;
            o_srfs <= 4'b0000;
        end
        else begin
            if(i_btn[0] && !btn_prev_state[0]) begin
                srfs_flag <= ~srfs_flag;
            end
            else begin
                case(i_btn[3:1] & ~btn_prev_state[3:1])
                    3'b100: color_sel <= 3'b100;
                    3'b010: color_sel <= 3'b010;
                    3'b001: color_sel <= 3'b001;
                    default: color_sel <= color_sel;
                endcase
            end
            o_srfs <= (srfs_flag) ? (flash) : (shift_reg);
 
            btn_prev_state <= i_btn;
        end
    end
            
    assign o_led[0] = srfs_flag;
    assign o_led[3:1] = color_sel;
    

    assign ledsRGB   = (color_sel == COLOR_SEL0) ? {o_srfs,{N_LEDS{1'b0}},{N_LEDS{1'b0}}}:
                       (color_sel == COLOR_SEL1) ? {{N_LEDS{1'b0}},o_srfs,{N_LEDS{1'b0}}}:
                                                   {{N_LEDS{1'b0}},{N_LEDS{1'b0}},o_srfs};
    assign o_led_r = ledsRGB[N_LEDS  -1 -: N_LEDS];
    assign o_led_g = ledsRGB[N_LEDS*2-1 -: N_LEDS];
    assign o_led_b = ledsRGB[N_LEDS*3-1 -: N_LEDS];


endmodule
