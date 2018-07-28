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
            self.buffer_in.insert(0,tx_in)
            self.buffer_in.pop()
            self.conv_shift = (self.conv_shift+1)%self.UPSAMPLE

    @property
    def tx_out(self):
        self._tx_out = self.conv()
        return self._tx_out
        
    
    def reset(self):
        self.buffer_in = [0]*self.BUFFER_IN_SIZE
        self.conv_shift = 0


    #Combinacional
    def conv(self):
        coef = self.coeficients[self.conv_shift::self.UPSAMPLE]
        values = self.buffer_in[self.conv_shift::self.UPSAMPLE]
        out_full = DeFixedInt(self.COEF_NBITS\
                                 + math.ceil(math.log(self.BUFFER_IN_SIZE,2)), 
                              self.COEF_FBITS)
        out = DeFixedInt(self.OUT_NBITS,self.OUT_FBITS)
        for c, v in zip(coef, values):
            if v==1: out_full.value = (out_full+c).fValue
            else: out_full.value = (out_full-c).fValue
        out.value = out_full.fValue
        return out
