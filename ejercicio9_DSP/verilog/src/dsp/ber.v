`define SEQ_LEN 1022
`define REG_LEN 64


module ber(
           clk,
           rst,
           enable,
           valid,
           sx,
           dx,
           error_flag,
           error_count,
           bit_count
           );

    parameter SEQ_LEN = `SEQ_LEN;

    localparam REG_LEN = `REG_LEN;
    localparam SHIFT_LEN = $clog2(SEQ_LEN);

    input clk;
    input rst;
    input enable;
    input valid;
    input sx;
    input dx;
    output error_flag;

    output reg [REG_LEN-1:0] error_count;
    output reg [REG_LEN-1:0] bit_count;
    reg [REG_LEN-1:0] min_error_count;
    reg [SHIFT_LEN-1:0] shift;
    reg [SHIFT_LEN-1:0] min_shift;
    reg [SHIFT_LEN-1:0] counter;
    reg [SEQ_LEN-1:0] buffer_in;
    reg adapt_flag;

    assign error_flag = (error_count != 0);

    always@(posedge clk or negedge rst)
    begin
        if (!rst) begin
            error_count <= {REG_LEN{1'b0}};
            bit_count <= {REG_LEN{1'b0}};
            min_error_count <= {REG_LEN{1'b1}};
            shift <= {SHIFT_LEN{1'b0}};
            min_shift <= {SHIFT_LEN{1'b0}};
            counter <= {SHIFT_LEN{1'b0}};
            buffer_in <= {SEQ_LEN{1'b0}};
            adapt_flag <= 1;
        end
        else begin
            if (enable & valid) begin
                buffer_in <= {sx, buffer_in[SEQ_LEN-1:1]};
                //adaptation
                if (adapt_flag) begin
                    if (counter < SEQ_LEN) begin
                        error_count <= error_count + (buffer_in[SEQ_LEN-1-shift] ^ dx);
                        counter <= counter + 1;
                    end
                    else begin
                        if (error_count < min_error_count) begin
                            min_error_count <= error_count;
                            min_shift <= shift;
                        end
                        counter <= 0;
                        error_count <= 0;
                        shift <= shift + 1;
                    end
                    if (shift == SEQ_LEN) begin
                        adapt_flag <= 0;
                        error_count <= 0;
                    end
                end
                //regimen
                else begin
                    error_count <= error_count + buffer_in[SEQ_LEN-1-min_shift] ^ dx;
                    bit_count <= bit_count + 1;
                end
            end
        end
    end
endmodule
