from tool._fixedInt import *

class tx(object):
    
    def __init__(self, COEF, UPSAMPLE, COEF_NBITS, COEF_FBITS, OUT_NBITS,
                 OUT_FBITS):

        self.UPSAMPLE = UPSAMPLE
        self.COEF_NBITS = COEF_NBITS
        self.COEF_FBITS = COEF_FBITS
        self.OUT_NBITS = OUT_NBITS
        self.OUT_FBITS = OUT_FBITS
        self.BUFFER_IN_SIZE = len(COEF)
        
        #initial
        self.coeficients = COEF



    def run(self, tx_in, enable):
        if enable:
            sum_a, sum_b = self.partial_sum()
            self._tx_out.value = (sum_a + sum_b).fValue
            self.buffer_in.insert(0,tx_in)
            self.buffer_in.pop()
            self.conv_shift = (self.conv_shift+1)%self.UPSAMPLE

    @property
    def tx_out(self):
        return self._tx_out
        
    
    def reset(self):
        self.buffer_in = [0]*self.BUFFER_IN_SIZE
        self.conv_shift = 0
        self._tx_out = DeFixedInt(self.OUT_NBITS,self.OUT_FBITS)


    #Combinacional
    def partial_sum(self):
        coef = self.coeficients[self.conv_shift::self.UPSAMPLE]
        values = self.buffer_in[self.conv_shift::self.UPSAMPLE]
        out_full_a = DeFixedInt(self.COEF_NBITS\
                                 + math.ceil(math.log(self.BUFFER_IN_SIZE,2)), 
                              self.COEF_FBITS)
        out_full_b = DeFixedInt(self.COEF_NBITS\
                                 + math.ceil(math.log(self.BUFFER_IN_SIZE,2)), 
                              self.COEF_FBITS)
        for c, v in zip(coef[::2], values[::2]):
            if v==1: out_full_a.value = (out_full_a+c).fValue
            else: out_full_a.value = (out_full_a-c).fValue
        for c, v in zip(coef[1::2], values[1::2]):
            if v==1: out_full_b.value = (out_full_b+c).fValue
            else: out_full_b.value = (out_full_b-c).fValue
        return out_full_a, out_full_b
