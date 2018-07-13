import numpy as np
import matplotlib.pyplot as plt
from commpy.filters import rrcosfilter, rcosfilter

from tool._fixedInt import *

SEQ_LEN = 511
NCLK = 4*SEQ_LEN
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

DX_SWITCH_SEL = 2


def prbs9(seed):    
    prbs_9 = int((seed & 0x001)>0)
    prbs_5 = int((seed & 0x010)>0)
    prbs = (((prbs_9^0b1^prbs_5)<<9) + seed>>1)
    return prbs


def conv_tx(coef, values, clk, offset, upsample):
    coef = coef[(clk+offset)%4::upsample]
    values = values[(clk+offset)%4::upsample]
    out = DeFixedInt(16,8)
    for c, v in zip(coef, values):
        if v==1: out.value = (out+c).fValue
        else: out.value = (out-c).fValue
    return out

def conv_rx(coef, values):
    out = DeFixedInt(16,8)
    for c, v in zip(coef, values):
        out.value = (out+(c*v)).fValue
    return out
    
    
    
def main():

    rst = 0
    rrcos = rrcosfilter(NBAUDS*UPSAMPLE, ROLL_OFF, 1./BAUD_RATE, SAMPLE_RATE)[1]
    rrcos = rrcos/np.sqrt(UPSAMPLE)
    rrcos_fixed = arrayFixedInt(16,8,rrcos)


    prbs_r_v = []
    prbs_i_v = []
    tx_r_v = []
    tx_i_v = []
    rx_r_v = []
    rx_i_v = []
    dx_r_v = []
    dx_i_v = []

    for clk in range(NCLK):
        if rst == 0:
            prbs_r = seed_r
            prbs_i = seed_i
            
            tx_r_in = [0]*NBAUDS*UPSAMPLE
            tx_i_in = [0]*NBAUDS*UPSAMPLE
            
            rx_r_in = [DeFixedInt(16,8)]*NBAUDS*UPSAMPLE
            rx_i_in = [DeFixedInt(16,8)]*NBAUDS*UPSAMPLE

            prbs_r_s = 0
            prbs_i_s = 0
            prbs_r_p = 0
            prbs_i_p = 0
            tx_r_s = DeFixedInt(16,8)
            tx_i_s = DeFixedInt(16,8)
            tx_r_p = DeFixedInt(16,8)
            tx_i_p = DeFixedInt(16,8)
            rx_r_s = DeFixedInt(16,8)
            rx_i_s = DeFixedInt(16,8)
            rx_r_p = DeFixedInt(16,8)
            rx_i_p = DeFixedInt(16,8)
            dx_r_s = 0
            dx_i_s = 0
            dx_r_p = 0
            dx_i_p = 0
            
            
            ber_counter = 0
            ber_tx_r_sr = [0]*2*SEQ_LEN
            ber_tx_i_sr = [0]*2*SEQ_LEN
            ber_dx_r = 0
            ber_dx_i = 0
            ber_shift = 0
            ber_error_count = 0
            ber_adapt_flag = True
            ber_min_error = 99999
            ber_min_shift = 0

        if clk == 0: rst = 1

        #FSM
        prbs9_enable = (clk % UPSAMPLE == 0)
        tx_enable = (clk%1==0)
        rx_enable = (clk%1==0)
        dx_enable = ((clk+DX_SWITCH_SEL) % UPSAMPLE == 0)


        #PRBS9
        if prbs9_enable:
            prbs_r = prbs9(prbs_r)
            prbs_i = prbs9(prbs_i)
        prbs_r_s = prbs_r%2
        prbs_i_s = prbs_i%2

        #TX (Tiene retardo)
        if tx_enable:
            #actualizo el buffer de entrada
            tx_r_in.insert(0, prbs_r_p)
            tx_r_in.pop()
            tx_i_in.insert(0, prbs_i_p)
            tx_i_in.pop()
            
            #realizo las convoluciones
            tx_r_s = conv_tx(rrcos_fixed, tx_r_in, clk, TX_OFFSET, UPSAMPLE)
            tx_i_s = conv_tx(rrcos_fixed, tx_i_in, clk, TX_OFFSET, UPSAMPLE)

        #RX (Tiene retardo)
        if rx_enable:
            rx_r_in.insert(0, tx_r_p)
            rx_r_in.pop()
            rx_i_in.insert(0, tx_i_p)
            rx_i_in.pop()

            #realizo las convoluciones
            rx_r_s = conv_rx(rrcos_fixed, rx_r_in)
            rx_i_s = conv_rx(rrcos_fixed, rx_i_in)
            

        #Slicer (No tiene retardo)
        if dx_enable:
            print rx_r_s.fValue
            dx_r_s = int(rx_r_s.fValue > 0)
            dx_i_s = int(rx_i_s.fValue > 0)
        

        """
            ber_counter = 0
            ber_tx_r_sr = [0]*2*SEQ_LEN
            ber_tx_i_sr = [0]*2*SEQ_LEN
            ber_dx = 0
            ber_shift = 0
            ber_error_count = 0
            ber_adapt_flag = True
            ber_min_error = 9999
            ber_min_shift = 0
        ber_enable = clk%4 == 0
        #BER Counter
        if ber_enable:

            #Etapa de adaptacion
            if ber_adapt_flag:
                if ber_counter<511:
                    ber_error_count += ber_tx_r_sr[ber_shift] ^ ber_dx_r
                    print ber_error_count, ber_tx_r_sr[ber_shift], ber_dx_r
                    ber_error_count += ber_tx_i_sr[ber_shift] ^ ber_dx_i
                    print ber_error_count, ber_tx_i_sr[ber_shift], ber_dx_i
                    import pdb; pdb.set_trace()
                    ber_counter += 1
                else:
                    #if ber_error_count == 0:
                    if ber_error_count < ber_min_error:
                        ber_min_error = ber_error_count

                        ber_min_shift = ber_shift
                    #ber_adapt_flag = False
                    #else:
                    ber_counter = 0
                    ber_error_count = 0
                    ber_shift += 1
                    print ber_min_shift, ber_min_error
                if ber_shift == 511:
                    ber_adapt_flag = False
            ber_tx_r_sr.insert(0, prbs_r_v[-1])
            ber_tx_r_sr.pop()
            ber_tx_i_sr.insert(0, prbs_i_v[-1])
            ber_tx_i_sr.pop()
            #print ber_error_count, ber_shift
        """


        #Actualizacion de los registros
        prbs_r_p = prbs_r_s
        prbs_i_p = prbs_i_s
        prbs_r_v.append(prbs_r_s)
        prbs_i_v.append(prbs_i_s)
        tx_r_p = tx_r_s
        tx_i_p = tx_i_s
        tx_r_v.append(tx_r_s)
        tx_i_v.append(tx_i_s)
        rx_r_p = rx_r_s
        rx_i_p = rx_i_s
        rx_r_v.append(rx_r_s)
        rx_i_v.append(rx_i_s)
        dx_r_p = dx_r_s
        dx_i_p = dx_i_s
        dx_r_v.append(dx_r_s)
        dx_i_v.append(dx_i_s)
                
                
            
            

    print prbs_r_v[0:80*4:4]
    print dx_r_v[::4][7:87]
    print np.array(prbs_r_v[0:-7*4:4]) ^ np.array(dx_r_v[::4][7:])
    print len(prbs_r_v[0:-7*4:4]), len(dx_r_v[::4][7:])
    plt.figure(0)
    plt.plot([i.fValue for i in tx_r_v[:200]])
    plt.figure(1)
    plt.plot([i.fValue for i in rx_r_v[:200]])
    plt.figure(2)
    plt.plot(dx_r_v, dx_i_v, '.')
    plt.show()
            


if __name__ == '__main__':
    main()
