import numpy as np

menu = "Seleccione una opcion: \n\n\
1 - Sumar \n\
2 - Restar \n\
3 - Multiplicar \n\
4 - Dividir \n\
5 - Iterativo \
"
iter_menu = "Seleccione el tipo de operacion iterativa \n\
    a - Suma \n\
    b - Resta \n\
    c - Multiplicacion\
"

def main():
    print menu
    try:
        operation = int(raw_input("Ingrese la operacion: "))

        if operation <= 4:
            op1 = float(raw_input("Ingrese el operando 1: "))
            op2 = float(raw_input("Ingrese el operando 2: "))

            if operation == 1:
                print "Resultado: ", op1+op2
            
            elif operation == 2:
                print "Resultado: ", op1-op2

            elif operation == 3:
                print "Resultado: ", op1*op2

            elif operation == 4:
                print "Resultado: ", op1/op2

        elif operation == 5:
            print iter_menu
            iter_operation = raw_input("Ingrese la operacion iterativa: ")
            if iter_operation not in ['a', 'b', 'c']:
                exit(1)
            iterations = int(raw_input("Ingrese la cantidad de iteraciones: "))
            value = float(raw_input("Ingrese el operando: "))

            if iter_operation == 'a':
                result = 0
                for i in range(iterations):
                    result += value

            if iter_operation == 'b':
                result = 0
                for i in range(iterations):
                    result -= value

            if iter_operation == 'c':
                result = 1
                for i in range(iterations):
                    result *= value
            
            print result

        else:
            exit(1)

    except:
        print "error"

            
            

if __name__ == '__main__':
    main()
