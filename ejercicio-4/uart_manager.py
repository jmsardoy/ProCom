import serial

class UartManager(object):
    
    def __init__(self):
        self.ser = serial.serial_for_url('loop://', timeout=1)
        self.ser.isOpen()
        self.ser.timeout=None
        self.ser.flushInput()
        self.ser.flushOutput()

    
    def send(self, data):
        frame = []

        #header
        frame.append(0xA0)
        data_len = len(data)
        if(data_len>15):
            frame[0] |=   0x10
            frame.append((data_len & 0xFF00)>>8)
            frame.append(data_len & 0x00FF)
        else:   
            frame[0] |= data_len
            frame.append(0)
            frame.append(0)

        frame.append(0) #campo Device

        #data
        for d in data:
            frame.append(ord(d))

        #tail
        frame.append(frame[0])
        for f in frame:
            self.ser.write(chr(f))
    

    def receive(self):
        header_str = self.ser.read(4)
        header = map(ord, header_str)

        if not header[0] & 0x10:
            data_len = header[0] & 0x0F
        else:
            data_len = header[1]<<8 | header[2]
        
        data = self.ser.read(data_len)

        tail = ord(self.ser.read(1))
        if header[0] != tail:
            print "El mensaje contiene errores"
            return
        return data

    def close(self):
        self.ser.close()


