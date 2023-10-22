from read_index import read_index #importamos funcion para leer un bloque de indice especifico
from write_index import write_index #importamos funcion para escribir un bloque de indice especifico
import sys
import json
import time

print(read_index(1))

def isFull(index:dict, len1: int, len2:int) -> bool: #evalua si un dict se llenó (considerando longitud de los que dict's que se hacen merge)
    return len(json.dumps(index).encode('utf-8'))>=len1 or len(json.dumps(index).encode('utf-8'))>=len2


def MergeBasico(index1:int, index2:int) -> None: #lo unico que hace es escribir
    posting1 = read_index(index1)
    posting2 = read_index(index2)

    # se calcula tamaño de cada posting
    len1 = len(json.dumps(posting1).encode('utf-8'))
    len2 = len(json.dumps(posting2).encode('utf-8'))


    print("posting1: ",posting1)
    print("posting2: ",posting2)
    print(len1)
    print(len2)

    #para nuevos diccionarios
    result1 = {} 
    result2 = {}

    # iteradores para cada posting list
    i1 = iter(posting1.items())
    i2 = iter(posting2.items())
    
    # definimos el inicio de cada posting (para empezar a recorrer)
    token1, valor1 = next(i1)
    token2, valor2 = next(i2)

    
    result1_full = False

    """ llenado del primer bloque """
    while not result1_full: #recorremos hasta que se llene r1
        if token1==token2: #terminos coinciden
            valor1.update(valor2)
            #print(valor1,valor2)
            result1[token1] = valor1 #añadimos merge de ambos posting list 
            
            # avanzamos ambos punteros
            token1, valor1 = next(i1)
            token2, valor2 = next(i2)

        elif token1<token2:
            result1[token1] = valor1 #añadimos menor

            # avanzamos puntero (del que acabamos de añadir -> token1)
            token1, valor1 = next(i1)

        else:
            result1[token2] = valor2

            # avanzamos puntero (del que acabamos de añadir -> token2)
            token2, valor2 = next(i2)

        result1_full = isFull(result1,len1,len2) 
        
        if result1_full:
            print("Se completó un bloque", result1)
            time.sleep(5)
    
            
    # en token1, token2 tengo elementos que aún no añado a ningun bloque resultante

    """ llenado del segundo bloque : la diferencia con este bloque, es que podemos llegar al final y por eso siempre usamos try """
    while True: 
        if token1==token2: #terminos coinciden
            valor1.update(valor2)
            result2[token1] = valor1 #añadimos merge de ambos posting list 
            
            # avanzamos ambos punteros
            try:
                token1, valor1 = next(i1)
                token2, valor2 = next(i2)
            except StopIteration: #se terminó de recorrer un diccionario
                break

        elif token1<token2: #añadimos el menor
            result2[token1] = valor1

            try:#intentamos seguir recorriendo el posting1
                token1, valor1 = next(i1)
            except StopIteration:
                break

        else:
            result2[token2] = valor2
        
            try: #intentamos seguir recorriendo el posting2
                token2, valor2 = next(i2)
            except StopIteration:
                break
        

    # añadimos posibles elementos resultantes (del posting1)
    while True:
        try:
            result2[token1] = valor1
            token1, valor1 = next(i1)
        except StopIteration:
            break

    # añadimos posibles elementos resultantes (del posting2)
    while True:
        try:
            result2[token2] = valor2
            token2, valor2 = next(i2)
        except StopIteration:
            break
            

    
    print("Bloques finales:")
    print("Bloque1: ",result1)

    print("\n\n\n")
    #time.sleep(10)
    print("Bloque2: ",result2)

    write_index(index1*100,result1)
    write_index(index2*100,result2)


for i in range (1,8,2): #prueba con primeros 4 pares de archivos
    MergeBasico(i,i+1)
#MergeBasico(3,4)
#MergeBasico(5,6)

