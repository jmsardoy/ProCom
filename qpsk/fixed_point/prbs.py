
class prbs(object):
    
    def __init__(self, SEED):
        self.SEED = SEED

    def run(self, enable):
        if enable:
            prbs_9 = int((self.buffer & 0x001)>0)
            prbs_5 = int((self.buffer & 0x010)>0)
            self.buffer = (((prbs_9^0b1^prbs_5)<<9) + self.buffer>>1)

    @property
    def prbs_out(self):
        return self.buffer%2

    def reset(self):
        self.buffer = self.SEED
