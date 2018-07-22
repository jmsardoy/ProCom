import numpy as np
import matplotlib.pyplot as plt
import math
from commpy.filters import rrcosfilter, rcosfilter

from tool._fixedInt import *
from tool.DSPtools import *

SEQ_LEN = 511
NCLK = 1*4*SEQ_LEN
#seed_r = 0b110101010
#seed_i = 0b111111110
seed_r = 0x1aa
seed_i = 0x1fe

ROLL_OFF = 0.5
NBAUDS = 6

UPSAMPLE = 4
BAUD_RATE = 25e6
SAMPLE_RATE = BAUD_RATE*UPSAMPLE

TX_OFFSET = 0

DX_SWITCH_SEL = 3


FILTER_N_BITS = 8
FILTER_F_BITS = 7

TX_N_BITS = 8
TX_F_BITS = 7

RX_N_BITS = 21
RX_F_BITS = 14

def prbs9(seed):    
    prbs_9 = int((seed & 0x001)>0)
    prbs_5 = int((seed & 0x010)>0)
    prbs = (((prbs_9^0b1^prbs_5)<<9) + seed>>1)
    return prbs


def conv_tx(coef, values, clk, offset, upsample):
    coef = coef[(clk+offset)%4::upsample]
    out_full = DeFixedInt(FILTER_N_BITS+math.ceil(math.log(NBAUDS,2)), 
                          FILTER_F_BITS)
    out = DeFixedInt(TX_N_BITS,TX_F_BITS)
    for c, v in zip(coef, values):
        if v==1: out_full.value = (out_full+c).fValue
        else: out_full.value = (out_full-c).fValue
    out.value = out_full.fValue
    return out

def conv_rx(coef, values):
    out_full = DeFixedInt(2*FILTER_N_BITS+math.ceil(math.log(NBAUDS*UPSAMPLE,2)),
                          2*FILTER_F_BITS)
    out = DeFixedInt(RX_N_BITS,RX_F_BITS)
    for c, v in zip(coef, values):
        out_full.value = (out_full+(c*v)).fValue
    out.value = out_full.fValue
    return out
    
    
    
def main():

    rst = 0
    rrcos = rrcosfilter(NBAUDS*UPSAMPLE, ROLL_OFF, 1./BAUD_RATE, SAMPLE_RATE)[1]
    rrcos = rrcos/np.sqrt(UPSAMPLE)
    rrcos_fixed = arrayFixedInt(FILTER_N_BITS,FILTER_F_BITS,rrcos)
    rrcos_pot = sum([i**2 for i in rrcos])
    error_pot = sum([(i.fValue-j)**2 for i,j in zip(rrcos_fixed, rrcos)])
    snr = 10*np.log10(error_pot/rrcos_pot)
    print snr
    symbols = []

    vector_r = []
    vector_i = []

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
            
            tx_r_in = [0]*NBAUDS
            tx_i_in = [0]*NBAUDS
            
            rx_r_in = [DeFixedInt(9,7)]*NBAUDS*UPSAMPLE
            rx_i_in = [DeFixedInt(9,7)]*NBAUDS*UPSAMPLE

            prbs_r_s = 0
            prbs_i_s = 0
            prbs_r_p = 0
            prbs_i_p = 0

            tx_r_s = DeFixedInt(9,7)
            tx_i_s = DeFixedInt(9,7)
            tx_r_p = DeFixedInt(9,7)
            tx_i_p = DeFixedInt(9,7)

            rx_r_s = DeFixedInt(9,7)
            rx_i_s = DeFixedInt(9,7)
            rx_r_p = DeFixedInt(9,7)
            rx_i_p = DeFixedInt(9,7)
            
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
        ber_enable = clk%UPSAMPLE == 0


        #PRBS9
        if prbs9_enable:
            prbs_r = prbs9(prbs_r)
            prbs_i = prbs9(prbs_i)
            symbols.append(2*(prbs_r%2)-1)
        else:
            symbols.append(0)
        prbs_r_s = prbs_r%2
        prbs_i_s = prbs_i%2

        #TX (Tiene retardo)
        if tx_enable:
            #actualizo el buffer de entrada
            #realizo las convoluciones
            tx_r_s = conv_tx(rrcos_fixed, tx_r_in, clk, TX_OFFSET, UPSAMPLE)
            tx_i_s = conv_tx(rrcos_fixed, tx_i_in, clk, TX_OFFSET, UPSAMPLE)

            if (clk%UPSAMPLE == 0):
                tx_r_in.insert(0, prbs_r_p)
                tx_r_in.pop()
                tx_i_in.insert(0, prbs_i_p)
                tx_i_in.pop()
            

        #RX (Tiene retardo)
        if rx_enable:
            #realizo las convoluciones
            rx_r_s = conv_rx(rrcos_fixed, rx_r_in)
            rx_i_s = conv_rx(rrcos_fixed, rx_i_in)

            rx_r_in.insert(0, tx_r_p)
            rx_r_in.pop()
            rx_i_in.insert(0, tx_i_p)
            rx_i_in.pop()
            

        #Slicer (No tiene retardo)
        if dx_enable:
            vector_r.append(rx_r_s.fValue)
            vector_i.append(rx_i_s.fValue)
            dx_r_s = int(rx_r_s.fValue > 0)
            dx_i_s = int(rx_i_s.fValue > 0)
        

        #BER Counter
        if ber_enable:

            #Actualizo el buffer de simbolos enviados
            ber_tx_r_sr.insert(0, prbs_r_p)
            ber_tx_r_sr.pop()
            ber_tx_i_sr.insert(0, prbs_i_p)
            ber_tx_i_sr.pop()
            #Etapa de adaptacion
            if ber_adapt_flag:
                if ber_counter<SEQ_LEN:
                    ber_error_count += ber_tx_r_sr[ber_shift] ^ dx_r_p
                    ber_error_count += ber_tx_i_sr[ber_shift] ^ dx_i_p
                    ber_counter += 1
                else:
                    print "............................."
                    print ber_shift, ber_error_count
                    print ber_min_shift, ber_min_error
                    if ber_error_count < ber_min_error:
                        ber_min_error = ber_error_count
                        ber_min_shift = ber_shift
                    ber_counter = 0
                    ber_error_count = 0
                    ber_shift += 1
                if ber_shift == 8:
                    ber_adapt_flag = False
                    ber_error_count = 0
            else:
                ber_error_count += ber_tx_r_sr[ber_min_shift] ^ dx_r_p
                ber_error_count += ber_tx_i_sr[ber_min_shift] ^ dx_i_p

                
                
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
                
                
            
    print [i.fValue for i in rx_r_v[:20]]
    import pdb; pdb.set_trace()
    tx_float = np.convolve(symbols, rrcos, 'same')       
    tx_pot = sum([i**2 for i in tx_float])
    tx_r = [i.fValue for i in tx_r_v[15:]]
    tx_error_pot = sum([(i-j)**2 for i,j in zip(tx_float, tx_r)])

    print 10*np.log10(tx_error_pot/tx_pot)

    rx_float = np.convolve(tx_float, rrcos, 'same')
    rx_pot = sum([i**2 for i in rx_float])
    rx_r = [i.fValue for i in rx_r_v[27:]]
    rx_error_pot = sum([(i-j)**2 for i,j in zip(rx_float, rx_r)])
    print 10*np.log10(rx_error_pot/rx_pot)
    
    plt.figure()
    plt.grid()
    plt.plot([i.fValue for i in tx_r_v[:200]])
    
    eyediagram([i.fValue for i in rx_r_v[12:]], 4, 1, UPSAMPLE)

    plt.figure()
    plt.grid()
    plt.plot([i.fValue for i in rx_r_v[:200]])

    rrcos_float = [i.fValue for i in rrcos_fixed]
    H,A,F = resp_freq(rrcos_float, 1./BAUD_RATE, 512)
    plt.figure()
    plt.grid()
    plt.semilogx(F, 20*np.log(H))

    plt.figure()
    plt.grid()
    plt.plot(vector_r, vector_i, '.')

    plt.show()

            


if __name__ == '__main__':
    main()
