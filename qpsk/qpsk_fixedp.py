import numpy as np
from commpy.filters import rrcosfilter, rcosfilter

from tool._fixedInt import *

NCLK = 4*512
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
tx_r_v = []
tx_i_v = []
tx_r_in = [0]*NBAUDS*UPSAMPLE
tx_i_in = [0]*NBAUDS*UPSAMPLE
rx_r_v = []
rx_i_v = []
rx_r_in = [0]*NBAUDS*UPSAMPLE
rx_i_in = [0]*NBAUDS*UPSAMPLE


def prbs9(seed):    
    prbs_9 = int((seed & 0x001)>0)
    prbs_5 = int((seed & 0x010)>0)
    prbs = (((prbs_9^0b1^prbs_5)<<9) + seed>>1)
    return prbs

def coef_mult(coef, values):
    print coef, values
    return np.inner(coef, values)
    
    
    
def main():
    prbs_r = seed_r
    prbs_i = seed_i

    rrcos = rrcosfilter(NBAUDS*UPSAMPLE, ROLL_OFF, 1./BAUD_RATE, SAMPLE_RATE)[1]
    rrcos = rrcos/np.sqrt(UPSAMPLE)
    rrcos_fixed = arrayFixedInt(32,16,rrcos)

    fvalues = [r.fValue for r in rrcos_fixed]

    for clk in range(NCLK):

        #FSM
        prbs9_enable = (clk%4==0)
        tx_enable = (clk%1==0)
        rx_enable = (clk%1==0)


        #PRBS9
        if prbs9_enable:
            prbs_r = prbs9(prbs_r)
            prbs_i = prbs9(prbs_i)
        prbs_r_v.append(prbs_r%2)
        prbs_i_v.append(prbs_i%2)

        #TX
        if tx_enable:
            coef = rrcos[clk%4::UPSAMPLE]
            values_r = tx_r_in[clk%4::UPSAMPLE]
            values_i = tx_i_in[clk%4::UPSAMPLE]
            tx_r_v.append(coef_mult(coef, values_r))
            tx_i_v.append(coef_mult(coef, values_i))
            tx_r_in.insert(0, prbs_r_v[-1])
            tx_r_in.pop()
            tx_i_in.insert(0, prbs_i_v[-1])
            tx_i_in.pop()

        if rx_enable:
            coef = rrcos[clk%4::UPSAMPLE]
            values_r = rx_r_in[clk%4::UPSAMPLE]
            values_i = rx_i_in[clk%4::UPSAMPLE]
            rx_r_v.append(coef_mult(coef, values_r))
            rx_i_v.append(coef_mult(coef, values_i))
            rx_r_in.insert(0, tx_r_v[-1])
            rx_r_in.pop()
            rx_i_in.insert(0, tx_i_v[-1])
            rx_i_in.pop()

    import pdb; pdb.set_trace()
            


if __name__ == '__main__':
    main()
