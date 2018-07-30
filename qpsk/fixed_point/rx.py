from tool._fixedInt import *

class rx(object):
    
    def __init__(self, COEF, UPSAMPLE, COEF_NBITS, COEF_FBITS, DATA_NBITS,
                 DATA_FBITS):
        self.UPSAMPLE = UPSAMPLE
        self.COEF = COEF
        self.COEF_NBITS = COEF_NBITS
        self.COEF_FBITS = COEF_FBITS
        self.DATA_NBITS = DATA_NBITS
        self.DATA_FBITS = DATA_FBITS
        self.NCOEF = len(COEF)
        self.MULT_NBITS = 2*COEF_NBITS
        self.OUT_FULL_NBITS = self.MULT_NBITS + math.ceil(math.log(self.NCOEF,2))


    @property
    def rx_out(self):
        return self._rx_out
        
    @property
    def rx_full_out(self):
        return self._rx_full_out

    def reset(self):
        self.coeficients = self.COEF
        self.filter_buffer = [DeFixedInt(self.OUT_FULL_NBITS, self.COEF_FBITS+self.DATA_FBITS)]*self.NCOEF
        self.clk_counter = 0
        self._rx_out = 0
        self._rx_full_out = self.filter_buffer[-1]


    def run(self, rx_in, phase_in, enable):

        if enable:
            if (self.clk_counter == phase_in):
                self._rx_out = int(self._rx_full_out.fValue >= 0)

            self._rx_full_out = self.filter_buffer[self.NCOEF-1]
            
            multiplication = self.multiplication(rx_in)
            filter_buffer_aux = [0]*self.NCOEF
            filter_buffer_aux[0] = multiplication[0]
            for i in range(1,len(self.filter_buffer)):
                filter_buffer_aux[i] = self.filter_buffer[i-1]+multiplication[i]
            self.filter_buffer = filter_buffer_aux
            self.clk_counter = (self.clk_counter+1)%self.UPSAMPLE


    #Combinacional
    def multiplication(self, rx_in):
        multiplication = []
        for coef in self.coeficients:
            multiplication.append(rx_in*coef)
        return multiplication
        
