`define SEED 0

module prbs(
            clk,
            rst,
            enable,
            valid,
            bit_out
            );
    parameter SEED = `SEED;
    
    output bit_out;
    input rst;
    input clk;
    input enable;
    input valid;

    reg [8 : 0] buffer;

    always@(posedge clk or negedge rst) begin
        if(!rst) begin
            buffer <= SEED;
        end
        else begin
            if (enable & valid) begin
                buffer <= {buffer[0]^buffer[4] , buffer[8:1]};
            end
        end
        
        
    end

    assign bit_out = buffer[0];

endmodule
