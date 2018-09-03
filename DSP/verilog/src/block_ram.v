module block_ram
#(
	parameter RAM_WIDTH = 32,
	parameter RAM_ADDR_NBIT = 15,
	parameter RAM_DEPTH = 2**RAM_ADDR_NBIT
 )
 (				 
	input clk,
	input i_run,
	input i_read,
	input [RAM_ADDR_NBIT -1 : 0] i_addr,
	input [RAM_WIDTH -1 : 0] i_data,
	output reg [ RAM_WIDTH -1 : 0] o_data,
	output reg o_mem_done
);

reg	run;
reg	[RAM_WIDTH -1 : 0] BRAM [RAM_DEPTH -1 : 0];
reg	[RAM_ADDR_NBIT -1 : 0] addr_counter;

always @(posedge clk ) begin
	if(addr_counter == RAM_DEPTH -1)begin
		addr_counter <= 0;
		o_mem_done <= 1;
	end
 	else if (i_run)begin
 		BRAM[addr_counter] <= i_data;
 		addr_counter <= addr_counter + 1;
 		o_mem_done<= 0;
 	end
 	else if((i_addr < RAM_DEPTH) && i_read) begin
 		o_data <= BRAM[i_addr];
 	end
 	else begin
 		addr_counter<=addr_counter;
 		o_data<={RAM_WIDTH{1'b0}};
 		o_mem_done <= o_mem_done;
 	end
 end



endmodule