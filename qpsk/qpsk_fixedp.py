import numpy as np
import matplotlib.pyplot as plt
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

TX_OFFSET = 3


prbs_r_v = []
prbs_i_v = []
tx_r_v = []
tx_i_v = []
tx_r_in = [0]*NBAUDS*UPSAMPLE
tx_i_in = [0]*NBAUDS*UPSAMPLE
rx_r_v = []
rx_i_v = []
rx_r_in = [DeFixedInt(32,16)]*NBAUDS*UPSAMPLE
rx_i_in = [DeFixedInt(32,16)]*NBAUDS*UPSAMPLE


def prbs9(seed):    
    prbs_9 = int((seed & 0x001)>0)
    prbs_5 = int((seed & 0x010)>0)
    prbs = (((prbs_9^0b1^prbs_5)<<9) + seed>>1)
    return prbs


def conv_tx(coef, values, clk, offset, upsample):
    coef = coef[(clk+offset)%4::upsample]
    values = values[(clk+offset)%4::upsample]
    out = DeFixedInt(32,16)
    for c, v in zip(coef, values):
        if v==1: out.value = (out+c).fValue
        else: out.value = (out-c).fValue
    return out

def conv_rx(coef, values):
    out = DeFixedInt(32,16)
    for c, v in zip(coef, values):
        out.value = (out+(c*v)).fValue
    return out
    
    
    
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
            tx_r_v.append(conv_tx(rrcos_fixed, tx_r_in, clk, TX_OFFSET, UPSAMPLE))
            tx_i_v.append(conv_tx(rrcos_fixed, tx_i_in, clk, TX_OFFSET, UPSAMPLE))
            tx_r_in.insert(0, prbs_r_v[-1])
            tx_r_in.pop()
            tx_i_in.insert(0, prbs_i_v[-1])
            tx_i_in.pop()

        if rx_enable:
            rx_r_v.append(conv_rx(rrcos_fixed, rx_r_in))
            rx_i_v.append(conv_rx(rrcos_fixed, rx_i_in))
            rx_r_in.insert(0, tx_r_v[-1])
            rx_r_in.pop()
            rx_i_in.insert(0, tx_i_v[-1])
            rx_i_in.pop()

    print prbs_r_v[:10]
    print tx_r_v[:10]
    print rx_r_v[:10]
    import pdb; pdb.set_trace()
    plt.figure(0)
    plt.plot([i.fValue for i in tx_r_v[:200]])
    plt.figure(1)
    plt.plot([i.fValue for i in rx_r_v[:200]])
    plt.show()
            


if __name__ == '__main__':
    main()
