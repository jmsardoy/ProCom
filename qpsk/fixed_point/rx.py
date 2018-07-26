from tool._fixedInt import *

class rx(object):
    
    def __init__(self, COEF, UPSAMPLE, COEF_NBITS, COEF_FBITS, DATA_NBITS,
                 DATA_FBITS):
        self.UPSAMPLE = UPSAMPLE
        self.COEF_NBITS = COEF_NBITS
        self.COEF_FBITS = COEF_FBITS
        self.DATA_NBITS = DATA_NBITS
        self.DATA_FBITS = DATA_FBITS
        self.BUFFER_IN_SIZE = len(COEF)

        #initial
        self.coeficients = COEF


    @property
    def rx_out(self):
        return self._rx_out
        
    @property
    def rx_full_out(self):
        self._rx_full_out = self.conv()
        return self._rx_full_out

    def reset(self):
        self.buffer_in = [DeFixedInt(self.DATA_NBITS,self.DATA_FBITS)]*self.BUFFER_IN_SIZE
        self.clk_counter = 0
        self._rx_out = 0
        self._rx_full_out = self.conv()


    def run(self, rx_in, phase_in):

        if (self.clk_counter == phase_in):
            self._rx_out = int(self.conv().fValue >= 0)
        self.buffer_in.insert(0,rx_in)
        self.buffer_in.pop()
        self.clk_counter = (self.clk_counter+1)%self.UPSAMPLE


    #Combinacional
    def conv(self):
        coef = self.coeficients
        values = self.buffer_in
        out_full = DeFixedInt(2*self.COEF_NBITS\
                                + math.ceil(math.log(self.BUFFER_IN_SIZE,2)),
                              2*self.COEF_FBITS)
        for c, v in zip(coef, values):
            out_full.value = (out_full+(c*v)).fValue
        return out_full

