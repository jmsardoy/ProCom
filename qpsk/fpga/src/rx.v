`define UPSAMPLE 4
`define NCOEF 24
`define COEF_NBITS 8
`define COEF_FBITS 7
`define DATA_NBITS 8

module rx(
          clk,
          rst,
          rx_in,
          phase_in,
          rx_out
          );
    

    parameter UPSAMPLE = `UPSAMPLE;
    parameter NCOEF = `NCOEF;
    parameter COEF = {NCOEF*COEF_NBITS{1'b0}};
    parameter COEF_NBITS = `COEF_NBITS;
    parameter COEF_FBITS = `COEF_FBITS;
    parameter DATA_NBITS = `DATA_NBITS;

    localparam BUFFER_IN_SIZE = NCOEF;
    localparam OUT_FULL_NBITS = 2*COEF_NBITS + $clog2(BUFFER_IN_SIZE)+8gtgt;
    localparam OUT_FULL_FBITS = 2*COEF_FBITS;


    input clk;
    input rst;
    input [DATA_NBITS-1:0] rx_in;
    input [$clog2(UPSAMPLE)-1:0] phase_in;
    
    output reg rx_out;


    reg signed [OUT_FULL_NBITS-1:0] rx_out_full;
    reg signed [DATA_NBITS-1:0] buffer_in [BUFFER_IN_SIZE-1:0];
    reg signed [COEF_NBITS-1:0] coeficients [0:NCOEF-1];
    reg [$clog2(UPSAMPLE)-1:0] clk_counter;
    integer i;

    assign reset = ~rst;


    initial begin
        for (i=0; i<NCOEF; i=i+1)
        begin
            coeficients[i] <= COEF[COEF_NBITS*NCOEF -1 -i*COEF_NBITS  -:
                                   COEF_NBITS];
        end
    end


    always@(posedge clk) 
    begin
    
        if(reset) begin
            clk_counter <= 0;
            for(i=0; i<BUFFER_IN_SIZE; i=i+1)
                buffer_in[i] <= {DATA_NBITS{1'b0}};
            rx_out = 0;
        end
        else begin
            clk_counter <= (clk_counter+1'b1)%UPSAMPLE;
            buffer_in[BUFFER_IN_SIZE-1] <= rx_in;
            for(i=0; i<BUFFER_IN_SIZE-1; i=i+1)
                buffer_in[i] <= buffer_in[i+1];
            if (clk_counter%UPSAMPLE == phase_in)
                rx_out <= ~rx_out_full[OUT_FULL_NBITS-1];
        end
    end


    always@* 
    begin
        //SUMA
        rx_out_full = {OUT_FULL_NBITS{1'b0}};
        for (i=0; i<BUFFER_IN_SIZE; i=i+1) begin
            rx_out_full = rx_out_full + (buffer_in[BUFFER_IN_SIZE-1-i]*coeficients[i]);
        end
    end


endmodule
