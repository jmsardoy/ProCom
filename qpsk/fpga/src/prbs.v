`define SEED 0

module prbs(
            clk,
            rst,
            bit_out
            );
    parameter SEED = `SEED;
    
    output bit_out;
    input rst;
    input clk;

    reg [8 : 0] buffer;
    wire        reset;

    assign reset = ~rst;


    always@(posedge clk or posedge reset) begin
        if(reset) begin
            buffer <= SEED;
        end
        else begin
            buffer <= {buffer[0]^buffer[4]^1'b1 , buffer[8:1]};
        end
        
        
    end

    assign bit_out = buffer[0];

endmodule
