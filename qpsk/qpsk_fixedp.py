import numpy as np
from commpy.filters import rrcosfilter, rcosfilter

from tool._fixedInt import *

NCLK = 4*513
#seed_r = 0b110101010
#seed_i = 0b111111110
seed_r = 0x1aa
seed_i = 0x1fe

LEN_SIGNALX = 511
ROLL_OFF = 0.5
NBAUDS = 6

UPSAMPLE = 4
BAUD_RATE = 25e6
SAMPLE_RATE = BAUD_RATE*UPSAMPLE


prbs_r_v = []
prbs_i_v = []


def prbs9(seed):    
    prbs_9 = int((seed & 0x001)>0)
    prbs_5 = int((seed & 0x010)>0)
    prbs = (((prbs_9^0b1^prbs_5)<<9) + seed>>1)
    return prbs
    
def main():
    prbs_r = seed_r
    prbs_i = seed_i

    rrcos = rrcosfilter(NBAUDS*UPSAMPLE, ROLL_OFF, 1./BAUD_RATE, SAMPLE_RATE)[1]
    rrcos = rrcos/np.sqrt(UPSAMPLE)
    rrcos_fixed = arrayFixedInt(32,16,rrcos)

    fvalues = [r.fValue for r in rrcos_fixed]
    for i in zip(rrcos, fvalues):
        print i

    tx_delay = 1
    rx_delay = 2
    

    for clk in range(NCLK):

        #FSM
        prbs9_enable = (clk%4==0)
        tx_enable = (clk%1==0)


        #PRBS9
        if prbs9_enable:
            prbs_r = prbs9(prbs_r)
            prbs_i = prbs9(prbs_i)
        prbs_r_v.append(prbs_r%2)
        prbs_i_v.append(prbs_i%2)

        #TX
        if tx_enable:
            coef = rrcos_fixed[clk%4::UPSAMPLE]
            print range(clk%4,24,UPSAMPLE)
            #print coef
            pass
            


if __name__ == '__main__':
    main()
