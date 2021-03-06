`define UPSAMPLE 4
`define NCOEF 24
`define COEF_NBITS 8
`define COEF_FBITS 7
`define DATA_NBITS 8

module rx(
          clk,
          rst,
          enable,
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
    localparam MULT_NBITS = 2*COEF_NBITS;
    localparam OUT_FULL_NBITS = 2*COEF_NBITS + $clog2(BUFFER_IN_SIZE);
    localparam OUT_FULL_FBITS = 2*COEF_FBITS;


    input clk;
    input rst;
    input enable;
    input signed [DATA_NBITS-1:0] rx_in;
    input [$clog2(UPSAMPLE)-1:0] phase_in;
    
    output reg rx_out;


    reg signed [OUT_FULL_NBITS-1:0] filter_buffer [NCOEF-1:0];
    reg signed [MULT_NBITS-1:0] multiplication [NCOEF-1:0];
    reg signed [COEF_NBITS-1:0] coeficients [NCOEF-1:0];
    reg [$clog2(UPSAMPLE)-1:0] clk_counter;
    integer i;

    assign reset = ~rst;


    always@(posedge clk) 
    begin
    
        if(reset) begin
            for (i=0; i<NCOEF; i=i+1) begin
                coeficients[i] <= COEF[COEF_NBITS*NCOEF -1 -i*COEF_NBITS  -: COEF_NBITS];
            end
            clk_counter <= 0;

            for(i=0; i<NCOEF; i=i+1) begin
                filter_buffer[i] <= {OUT_FULL_NBITS{1'b0}};
            end

            for(i=0; i<NCOEF; i=i+1) begin
             multiplication[i] <= {OUT_FULL_NBITS{1'b0}};
            end
            rx_out <= 0;
        end
        else begin
            if (enable) begin
                if (clk_counter == UPSAMPLE-1) 
                    clk_counter <= 0;
                else
                    clk_counter <= clk_counter+1;

                for (i=0; i<NCOEF; i=i+1) begin
                    multiplication[i] <= rx_in*coeficients[i];
                end

                filter_buffer[0] <= multiplication[0];
                for(i=1; i<NCOEF; i=i+1) begin
                    filter_buffer[i] <= filter_buffer[i-1]+multiplication[i];
                end
                if (clk_counter == phase_in)
                    rx_out <= ~filter_buffer[NCOEF-1][OUT_FULL_NBITS-1];
            end
            else begin
                clk_counter <= clk_counter;
                for (i=0; i<NCOEF; i=i+1) begin
                    multiplication[i] <= multiplication[i];
                    filter_buffer[i] <= filter_buffer[i];
                    rx_out <= rx_out;
                end

            end
        end
    end



endmodule
