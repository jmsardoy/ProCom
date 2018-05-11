import numpy as np

menu = "---------------------\n\
Seleccione una opcion: \n\n\
1 - Sumar \n\
2 - Restar \n\
3 - Multiplicar \n\
4 - Dividir \n\
5 - Iterativo \n\
6 - Producto Punto \n\
"
iter_menu = "Seleccione el tipo de operacion iterativa \n\
    a - Suma \n\
    b - Resta \n\
    c - Multiplicacionn\
"


matrix_help = "Ingrese las matrices en el siguiente formato: \n\
    filas separadas por ';'\n\
    elementos separados por ','\n\
\n\
ej:  1 2 3\n\
     3 4 5\n\
     6 7 8\n\
\n\
     1 , 2 , 3 ; 4 , 5 , 6 ; 7 , 8 , 9\n\
"
def calc():
    keep_calc = True
    while keep_calc:
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
                iterations = int(raw_input("Ingrese " +  
                                           "la cantidad de iteraciones: "))
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

            elif operation == 6:
                success_flag = False
                while not success_flag:
                    print matrix_help
                    matrix1 = raw_input("Ingrese Matriz 1: ")
                    matrix2 = raw_input("Ingrese Matriz 2: ")
                    try:
                        matrix1 = matrix1.split(';')
                        matrix2 = matrix2.split(';')
                        matrix1 = [i.split(',') for i in matrix1]
                        matrix2 = [i.split(',') for i in matrix2]
                        matrix1 = [[float(i) for i in j] for j in matrix1]
                        matrix2 = [[float(i) for i in j] for j in matrix2]
                        matrix1 = np.array(matrix1)
                        matrix2 = np.array(matrix2)
                        res = np.dot(matrix1,matrix2)
                        print res
                        success_flag = True
                    except:
                        print "Error en el formato o en las dimensiones"
            else:
                exit(1)
        except:   
            print "error\n"

        keep_calc_input = ''
        while keep_calc_input not in ['y','n']:
            keep_calc_input = raw_input("Seguir operando y/n: ")
        keep_calc = (keep_calc_input == 'y')
            

if __name__ == '__main__':
    calc|()
