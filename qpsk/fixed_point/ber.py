

class ber(object):
    
    def __init__(self, SEQ_LEN):
        self.SEQ_LEN = SEQ_LEN

    @property
    def error_count(self):
        return self._error_count


    def reset(self):
        self._error_count = 0
        self.min_error_count = 9999999
        self.shift = 0
        self.min_shift = 0
        self.adapt_flag = 1
        self.counter = 0
        self.buffer_in = [0]*self.SEQ_LEN*2


    def run(self, sx, dx):
        if self.adapt_flag:  
            if self.counter<self.SEQ_LEN:
                self._error_count += self.buffer_in[self.shift] ^ dx
                self.counter += 1
            else:
                print "............................."
                print self.shift, self._error_count
                print self.min_shift, self.min_error_count
                if self._error_count < self.min_error_count:
                    self.min_error_count = self._error_count
                    self.min_shift = self.shift
                self.counter = 0
                self._error_count = 0
                self.shift += 1
            if self.shift == self.SEQ_LEN:
                self.adapt_flag = 0
                self._error_count = 0
        else:
            self._error_count += self.buffer_in[self.min_shift] ^ dx
        self.buffer_in.insert(0, sx)
        self.buffer_in.pop()

        
