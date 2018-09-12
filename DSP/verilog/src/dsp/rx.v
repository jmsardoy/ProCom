`define UPSAMPLE 4
`define NCOEF 24
`define COEF_NBITS 8
`define COEF_FBITS 7
`define DATA_NBITS 8
`define OUT_NBITS 8
`define OUT_FBITS 7

module rx(
          clk,
          rst,
          enable,
          rx_in,
          phase_in,
          rx_out,
          rx_bit_out
          );
    

    parameter UPSAMPLE = `UPSAMPLE;
    parameter NCOEF = `NCOEF;
    parameter COEF = {NCOEF*COEF_NBITS{1'b0}};
    parameter COEF_NBITS = `COEF_NBITS;
    parameter COEF_FBITS = `COEF_FBITS;
    parameter DATA_NBITS = `DATA_NBITS;
    parameter OUT_NBITS = `OUT_NBITS;
    parameter OUT_FBITS = `OUT_FBITS;

    localparam BUFFER_IN_SIZE = NCOEF;
    localparam MULT_NBITS = 2*COEF_NBITS;
    localparam OUT_FULL_NBITS = 2*COEF_NBITS + $clog2(BUFFER_IN_SIZE);
    localparam OUT_FULL_FBITS = 2*COEF_FBITS;
    localparam OUT_SHIFT = OUT_NBITS - OUT_FBITS - 1;


    input clk;
    input rst;
    input enable;
    input signed [DATA_NBITS-1:0] rx_in;
    input [$clog2(UPSAMPLE)-1:0] phase_in;
    
    output reg signed [OUT_NBITS - 1 : 0] rx_out;
    output reg rx_bit_out;

    reg  sat_flag;
    reg  signed [OUT_FULL_NBITS - 1 : 0] rx_out_full;

    reg signed [OUT_FULL_NBITS-1:0] filter_buffer [NCOEF-1:0];
    reg signed [MULT_NBITS-1:0] multiplication [NCOEF-1:0];
    reg signed [COEF_NBITS-1:0] coeficients [NCOEF-1:0];
    reg [$clog2(UPSAMPLE)-1:0] clk_counter;
    integer i;


    always@(posedge clk or negedge rst) 
    begin
    
        if(!rst) begin
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
            rx_out_full <= 0;
            rx_bit_out <= 0;
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
                if (clk_counter == phase_in) begin
                    rx_bit_out <= ~filter_buffer[NCOEF-1][OUT_FULL_NBITS-1];
                end
                rx_out_full <= filter_buffer[NCOEF-1];
            end
            else begin
                clk_counter <= clk_counter;
                for (i=0; i<NCOEF; i=i+1) begin
                    multiplication[i] <= multiplication[i];
                    filter_buffer[i] <= filter_buffer[i];
                end
                rx_bit_out <= rx_bit_out;
                rx_out_full <= rx_out_full;

            end
        end
    end

    //SATURACION
    always@*
    begin
        sat_flag = 0;
        for (i=OUT_FULL_FBITS+OUT_SHIFT; i<OUT_FULL_NBITS-1; i=i+1)
            if(rx_out_full[i]^rx_out_full[i+1])
                sat_flag = 1;
        if (sat_flag) begin
            if (rx_out_full[OUT_FULL_NBITS-1])
                rx_out = {1'b1, {OUT_NBITS-1{1'b0}}};
            else
                rx_out = {1'b0, {OUT_NBITS-1{1'b1}}};
        end
        else 
            rx_out = rx_out_full[OUT_FULL_FBITS+OUT_SHIFT : OUT_FULL_FBITS - OUT_FBITS];
    end


endmodule
