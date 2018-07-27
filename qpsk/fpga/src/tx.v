`define UPSAMPLE 4
`define NCOEF 24
`define COEF_NBITS 8
`define COEF_FBITS 7
`define OUT_NBITS 8
`define OUT_FBITS 7

module tx(
          clk,
          rst,
          enable,
          tx_in,
          tx_out
          );
    

    parameter UPSAMPLE = `UPSAMPLE;
    parameter NCOEF = `NCOEF;
    parameter COEF = {NCOEF*COEF_NBITS{1'b0}};
    parameter COEF_NBITS = `COEF_NBITS;
    parameter COEF_FBITS = `COEF_FBITS;
    parameter OUT_NBITS = `OUT_NBITS;
    parameter OUT_FBITS = `OUT_FBITS;

    localparam BUFFER_IN_SIZE = NCOEF;
    localparam OUT_FULL_NBITS = COEF_NBITS + $clog2(BUFFER_IN_SIZE);
    localparam OUT_FULL_FBITS = COEF_FBITS;
    localparam OUT_SHIFT = OUT_NBITS - OUT_FBITS - 1;


    input clk;
    input rst;
    input enable;
    input tx_in;
    
    output reg[OUT_NBITS-1:0] tx_out;


    reg signed [OUT_FULL_NBITS-1:0] tx_out_full;
    reg [BUFFER_IN_SIZE-1:0] buffer_in;
    reg signed [COEF_NBITS-1:0] coeficients [0:NCOEF-1];
    reg [$clog2(UPSAMPLE)-1:0] conv_shift;
    reg  sat_flag;
    integer i;


    assign reset = ~rst;


    always@(posedge clk or posedge reset) 
    begin
    
        if(reset) begin
            for (i=0; i<NCOEF; i=i+1) begin
                coeficients[i] <= COEF[COEF_NBITS*NCOEF -1 -i*COEF_NBITS -: COEF_NBITS];
            end
            conv_shift <= 0;
            buffer_in <= {BUFFER_IN_SIZE{1'b0}};
        end
        else begin
            if (enable) begin
                if (conv_shift == UPSAMPLE-1)
                    conv_shift <= 0;
                else
                    conv_shift <= (conv_shift+1'b1);
                buffer_in <= {tx_in, buffer_in[BUFFER_IN_SIZE-1:1]};
            end
        end
    end


    always@* 
    begin
        tx_out_full = {OUT_FULL_NBITS{1'b0}};
        if (enable) begin
            //SUMA
            for (i=0; i<NCOEF/UPSAMPLE; i=i+1) begin
                if(buffer_in[BUFFER_IN_SIZE-1-(i*UPSAMPLE+conv_shift)])
                    tx_out_full = tx_out_full + coeficients[i*UPSAMPLE+conv_shift];
                else
                    tx_out_full = tx_out_full - coeficients[i*UPSAMPLE+conv_shift];
            end
        end

        //SATURACION
        sat_flag = 0;
        for (i=OUT_FULL_FBITS+OUT_SHIFT; i<OUT_FULL_NBITS-1; i=i+1)
            if(tx_out_full[i]^tx_out_full[i+1])
                sat_flag = 1;
        if (sat_flag) begin
            if (tx_out_full[OUT_FULL_NBITS-1])
                tx_out = {1'b1, {OUT_NBITS-1{1'b0}}};
            else
                tx_out = {1'b0, {OUT_NBITS-1{1'b1}}};
        end
        else 
            tx_out = tx_out_full[OUT_FULL_FBITS+OUT_SHIFT : COEF_FBITS - OUT_FBITS];
    end



endmodule
