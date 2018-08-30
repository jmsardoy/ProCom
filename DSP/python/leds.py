from uart_manager import UartManager



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
    
    uart = UartManager('/dev/ttyUSB2', 115200)
    
    def strcolor2bits(str_color):
        out_bits = 0x0
        for c in str_color[::-1]:
            if c == '-':
                out_bits = out_bits<<1;
            else:
                out_bits = out_bits<<1 | 1;
        return out_bits
        
    while(True):
        inp = -1
        while inp not in main_menu_choices:
            inp = raw_input(main_menu)
        if inp == '0':
            inp = -1
            while inp not in leds_menu_choices:
                inp = raw_input(leds_menu)
            led_choice = int(inp)
            while inp not in colors_menu_choices:
                inp = raw_input(colors_menu)
            bits = strcolor2bits(inp)
            data = chr(led_choice<<4 | bits)
            uart.send(0, data)
            print "enviado"
        else:
            uart.send(1, '')
            print uart.receive()


if __name__ == '__main__':
    main()
