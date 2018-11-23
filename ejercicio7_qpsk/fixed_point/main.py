import numpy as np
import matplotlib.pyplot as plt

from commpy.filters import rrcosfilter, rcosfilter
from tool.DSPtools import *

from tool._fixedInt import *
from prbs import prbs
from tx import tx
from rx import rx
from ber import ber

SEQ_LEN = 511
NCLK =1*4*SEQ_LEN

SEED_R = 0x1aa
SEED_I = 0x1fe

ROLL_OFF = 0.5
NBAUDS = 6

UPSAMPLE = 4
BAUD_RATE = 25e6
SAMPLE_RATE = BAUD_RATE*UPSAMPLE


DX_SWITCH_SEL = 2

COEF_NBITS = 8
COEF_FBITS = 7

TX_NBITS = 8
TX_FBITS = 7


def main():

    rrcos = rrcosfilter(NBAUDS*UPSAMPLE, ROLL_OFF, 1./BAUD_RATE, SAMPLE_RATE)[1]
    rrcos = rrcos/np.sqrt(UPSAMPLE)
    rrcos_fixed = arrayFixedInt(COEF_NBITS,COEF_FBITS,rrcos)


    prbs_r = prbs(SEED_R)
    tx_r = tx(rrcos_fixed, UPSAMPLE, COEF_NBITS, COEF_FBITS, TX_NBITS, TX_FBITS)
    rx_r = rx(rrcos_fixed, UPSAMPLE, COEF_NBITS, COEF_FBITS, TX_NBITS, TX_FBITS)
    ber_r = ber(SEQ_LEN)


    rrcos_float = [i.fValue for i in rrcos_fixed]

    prbs_r_v = []
    tx_r_v = []
    rx_r_v = []
    rx_full_v = []


    prbs_r.reset()
    tx_r.reset()
    rx_r.reset()
    ber_r.reset()


    phase = DX_SWITCH_SEL
    prbs_r_s = prbs_r.prbs_out
    tx_r_s = tx_r.tx_out
    rx_r_s = rx_r.rx_out
    

    enable_prbs = 0
    enable_tx = 1
    enable_rx = 1
    enable_ber = 0

    counter = 0


    for i in range(NCLK):


        prbs_r_s = prbs_r.prbs_out
        tx_r_s = tx_r.tx_out
        rx_r_s = rx_r.rx_out
        rx_full_out = rx_r.rx_full_out

        prbs_r_v.append(prbs_r_s)
        tx_r_v.append(tx_r_s.fValue)
        rx_r_v.append(rx_r_s)
        rx_full_v.append(rx_full_out.fValue)

        prbs_r.run(enable_prbs)
        ber_r.run(prbs_r_s, rx_r_s, enable_ber)
        rx_r.run(tx_r_s, phase, enable_rx)
        tx_r.run(prbs_r_s, enable_tx)

        if counter == 0:
            enable_prbs = 1
            enable_ber = 1
        else:
            enable_prbs = 0
            enable_ber = 0
        counter = (counter+1)%4


    vector = zip(range(NCLK),prbs_r_v, tx_r_v, rx_full_v, rx_r_v)
    """
    for i in vector[0:20]:
        print i
    exit()
    """

    plt.figure()
    plt.grid()
    plt.plot(tx_r_v[:200])


    plt.figure()
    plt.grid()
    plt.plot(rx_full_v[:200])
    rx_a= arrayFixedInt(8,7, rx_full_v[:200])
    rx_a = [i.fValue for i in rx_a]
    plt.figure()
    plt.grid()
    plt.plot(rx_a)


    """
    eyediagram(rx_full_v[12:], 4, 1, UPSAMPLE)

    rrcos_float = [i.fValue for i in rrcos_fixed]
    H,A,F = resp_freq(rrcos_float, 1./BAUD_RATE, 512)
    plt.figure()
    plt.grid()
    plt.semilogx(F, 20*np.log(H))

    plt.figure()
    plt.grid()
    plt.plot([i.fValue for i in rrcos_fixed])
    """

    plt.show()


if __name__ == '__main__':
    main()
