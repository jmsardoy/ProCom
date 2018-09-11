from uart_manager import UartManager
from time import sleep



def main():
    
    main_menu  =   "Escribir - 0 \n"\
                 + "Leer     - 1 \n"\
                 + "Input: "
    leds_menu =    "Elija el led a escribir (0-3)\n"\
                 + "Input: "
    colors_menu =  "Elija el color en formato rgb \n"\
                 + "Ejemplo: 'r-b' \n"\
                 + "Input: "
    
    main_menu_choices = ['0','1']
    leds_menu_choices = ['0','1','2','3']
    colors_menu_choices = ['---','--b','-g-', '-gb',
                         'r--','r-b','rg-', 'rgb']
    
    uart = UartManager('/dev/ttyUSB1', 115200)
    
    def strcolor2bits(str_color):
        out_bits = 0x0
        for c in str_color[::-1]:
            if c == '-':
                out_bits = out_bits<<1;
            else:
                out_bits = out_bits<<1 | 1;
        return out_bits
        
    uart.send(0, '')
    uart.send(1, '')
    uart.send(2, '')
    uart.send(3, '')
    sleep(0.2)
    while(True):
        device = int(raw_input(":"))
        uart.send(device, '')
        lala =  uart.receive()
        print lala
        print len(lala[1])

if __name__ == '__main__':
    main()
