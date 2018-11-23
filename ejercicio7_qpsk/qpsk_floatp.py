import numpy as np
import matplotlib.pyplot as plt
from commpy.filters import rrcosfilter, rcosfilter

from tool.DSPtools import *

LEN_PLOT = 200

LEN_SIGNALX = 511
ROLL_OFF = 0.5
NBAUDS = 6

UPSAMPLE = 4
BAUD_RATE = 25e6
SAMPLE_RATE = BAUD_RATE*UPSAMPLE


def main():
    #generacion random
    x_re = np.random.randint(0,2,LEN_SIGNALX)*2-1
    x_im = np.random.randint(0,2,LEN_SIGNALX)*2-1
    x_signal = zip(x_re, x_im)

    #upsample
    len_upsampled = UPSAMPLE*LEN_SIGNALX
    up_x_re = np.zeros(len_upsampled)
    up_x_re[np.array(range(LEN_SIGNALX))*UPSAMPLE] = x_re
    up_x_im = np.zeros(len_upsampled)
    up_x_im[np.array(range(LEN_SIGNALX))*UPSAMPLE] = x_im
    
    #rrcos filter
    rrcos = rrcosfilter(NBAUDS*UPSAMPLE, ROLL_OFF, 1./BAUD_RATE, SAMPLE_RATE)[1]
    rrcos = rrcos/np.sqrt(UPSAMPLE)
    H,A,F = resp_freq(rrcos, 1./BAUD_RATE, 256)
    plt.figure()
    plt.grid()
    plt.title('root raised cosine')
    plt.plot(rrcos)
    plt.figure()
    plt.grid()
    plt.semilogx(F, 20*np.log(H))
    
    #senial enviada
    tx_re = np.convolve(up_x_re, rrcos, 'same')
    tx_im = np.convolve(up_x_im, rrcos, 'same')
    plt.figure()
    plt.grid()
    plt.title('tx signal real')
    plt.plot(tx_re[:LEN_PLOT])

    #senial recibida
    rx_re = np.convolve(tx_re, rrcos, 'same')
    rx_im = np.convolve(tx_im, rrcos, 'same')
    plt.figure()
    plt.grid()
    plt.title('rx signal real')
    plt.plot(rx_re[:LEN_PLOT])
    eyediagram(rx_re, 4, 2, UPSAMPLE)

    #downsample
    offset = 2
    sample_indexs = range(offset, len(rx_re), UPSAMPLE)
    down_rx_re = rx_re[sample_indexs]
    down_rx_im = rx_im[sample_indexs]
    plt.figure()
    plt.title('recibed symbols')
    plt.grid()
    plt.plot(down_rx_re, down_rx_im, '.')
    
    #slicer
    detection_re = (down_rx_re>0)*2-1
    detection_im = (down_rx_im>0)*2-1
    detection = zip(detection_re, detection_im)
    plt.show(block=False)
    raw_input("Aprete cualquier tecla")
    plt.close()


if __name__ == '__main__':
    main()


