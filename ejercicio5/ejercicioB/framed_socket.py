import socket

class FramedSocket(socket.socket):
    
    def send(data):
        data = self.construct_frame(data)
        super(FramedSocket, self).send(data)

    def recv(size):
        frame = super(FramedSocket, self).recv(size)
        return self.read_frame(frame)
        

    def construct_frame(self, data):
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
        frame = map(chr, frame)
        frame.append(data)
        frame.append(frame[0])
        frame = ''.join(frame)
        return frame

    def read_frame(self, frame):
        header_str = frame[:4]
        header = map(ord, header_str)

        if not header[0] & 0x10:
            data_len = header[0] & 0x0F
        else:
            data_len = header[1]<<8 | header[2]

        data = frame[4:data_len+4]
        tail = ord(frame[data_len+4])
        if header[0] != tail:
            print "El mensaje contiene errores"
            return
        return data
