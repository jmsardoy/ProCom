import time
import serial
import matplotlib.pyplot as plt
import numpy as np

from calculadora import calc
from figplot import figplot
from uart_manager import UartManager


############################################
# Nota:
# Comentar esta linea si se utiliza el puerto serie
# con la FPGA

#############################################
# Nota:
# Descomentar esta linea si se utiliza el puerto serie
# con la FPGA
#############################################
# ser = serial.Serial(
#     port     = '/dev/ttyUSB1',
#     baudrate = 9600,
#     parity   = serial.PARITY_NONE,
#     stopbits = serial.STOPBITS_ONE,
#     bytesize = serial.EIGHTBITS
# )


uart = UartManager()

while True:
    print 'Ingrese opcion (calculador - graficar- exit):'
    data = raw_input("opction: ")
    uart.send(data)
    out =  uart.receive()
    if out == 'calculadora':
        calc()
    elif out == 'graficar':
        x_params = raw_input("ingrese x_init, x-end, step separado por " +
                             "espacios: ").split(" ")
        y_params = raw_input("ingrese y_init, y-end, step separado por " +
                             "espacios: ").split(" ")
        x_init, x_end, x_step = map(float, x_params)
        y_init, y_end, y_step = map(float, y_params)
        xlim = [(x_init, x_end)]
        ylim = [(y_init, y_end)]
        x = [np.arange(x_init, x_end, x_step)]
        y = [np.arange(y_init, y_end, y_step)]
        figplot(x,y, 1, 1, 1, [plt.plot], xlim, xlim, 'xlabel', 'ylabel',
                show=True)
    elif out == 'exit':
        uart.close()
        exit()
    else:
        print "comando incorrecto"
        
