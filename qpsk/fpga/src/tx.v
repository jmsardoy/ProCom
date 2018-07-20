`define UPSAMPLE 4
`define NCOEF 24
`define COEF_NBITS 8
`define COEF_FBITS 6
`define OUT_NBITS 7
`define OUT_FBITS 6

module tx(
          clk,
          rst,
          tx_in,
          tx_out
          );
    

    parameter UPSAMPLE = `UPSAMPLE;
    parameter NCOEF = `NCOEF;
    parameter COEF_NBITS = `COEF_NBITS;
    parameter COEF_FBITS = `COEF_FBITS;
    parameter OUT_NBITS = `OUT_NBITS;
    parameter OUT_FBITS = `OUT_FBITS;
    parameter COEF = {NCOEF*COEF_NBITS{1'b0}};

    localparam BUFFER_IN_SIZE = NCOEF/UPSAMPLE;
    localparam OUT_FULL_NBITS = COEF_NBITS + $clog2(BUFFER_IN_SIZE);


    input clk;
    input rst;
    input tx_in;
    
    output reg[OUT_NBITS-1:0] tx_out;


    reg signed [OUT_FULL_NBITS-1:0] tx_out_full;
    reg [BUFFER_IN_SIZE-1:0] buffer_in;
    reg signed [COEF_NBITS-1:0] coeficients [0:NCOEF-1];
    reg [$clog2(UPSAMPLE)-1:0] clk_counter;
    reg  sat_flag;
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
            buffer_in <= {BUFFER_IN_SIZE{1'b0}};
        end
        else begin
            clk_counter <= (clk_counter+1'b1)%UPSAMPLE;
            if (clk_counter == 0)
                buffer_in <= {tx_in, buffer_in[5:1]};
        end
    end


    always@* 
    begin
        //SUMA
        tx_out_full = {OUT_FULL_NBITS{1'b0}};
        for (i=0; i<BUFFER_IN_SIZE; i=i+1) begin
            if(buffer_in[BUFFER_IN_SIZE-1-i])
                tx_out_full = tx_out_full + coeficients[i*UPSAMPLE+clk_counter];
            else
                tx_out_full = tx_out_full - coeficients[i*UPSAMPLE+clk_counter];
        end

        //SATURACION
        sat_flag = 0;
        for(i=OUT_NBITS-1; i<OUT_FULL_NBITS-1; i=i+1)
            if(tx_out_full[i]^tx_out_full[i+1])
                sat_flag = 1;
        if (sat_flag) begin
            if (tx_out_full[OUT_FULL_NBITS-1])
                tx_out = { {OUT_NBITS-OUT_NBITS{1'b1}}, {OUT_FBITS{1'b0}}};
            else
                tx_out = { {OUT_NBITS-OUT_FBITS{1'b0}}, {OUT_FBITS{1'b1}}};
        end
        else
            tx_out = tx_out_full[COEF_FBITS-OUT_FBITS+OUT_NBITS-1 -: OUT_NBITS-1];
    end



endmodule
