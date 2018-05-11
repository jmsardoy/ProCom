import time
import serial

#############################################
# Nota:
# Comentar esta linea si se utiliza el puerto serie
# con la FPGA
ser = serial.serial_for_url('loop://', timeout=1)

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

ser.isOpen()
ser.timeout=None
ser.flushInput()
ser.flushOutput()
print(ser.timeout)

print 'Ingrese un comando:\n'
while 1 :
    char_v = []
    input = raw_input("ToSent: ")
    if (input == 'exit'):
        ser.close()
        exit()
    else:
        # Arma el vector a transmitir
        for ptr in range(len(input)):
            char_v.append(input[ptr])

        for ptr in range(len(char_v)):
            ser.write(char_v[ptr])
            time.sleep(1)

        out = ''

        while ser.inWaiting() > 0:
            out += ser.read(1)

        if out != '':
            print ">> " + out
