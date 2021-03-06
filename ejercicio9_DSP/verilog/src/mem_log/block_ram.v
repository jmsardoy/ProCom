module block_ram
#(
	parameter RAM_WIDTH = 32,
	parameter RAM_ADDR_NBIT = 15
 )
 (				 
	input clk,
	input i_write_enable,
	input i_read_enable,
	input [RAM_ADDR_NBIT - 1 : 0] i_write_addr,
	input [RAM_ADDR_NBIT - 1 : 0] i_read_addr,
	input [RAM_WIDTH -1 : 0] i_data,
	output reg [ RAM_WIDTH -1 : 0] o_data
);

	localparam RAM_DEPTH = 2**RAM_ADDR_NBIT;

    reg	[RAM_WIDTH - 1 : 0] bram [RAM_DEPTH - 1 : 0];

    always@(posedge clk) begin
        if (i_write_enable) bram[i_write_addr] <= i_data;
        if (i_read_enable) o_data <= bram[i_read_addr];
    end


endmodule
