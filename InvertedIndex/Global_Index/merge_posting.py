from read_index import read_index #importamos funcion para leer un bloque de indice especifico
from write_index import write_index #importamos funcion para escribir un bloque de indice especifico
import sys
import json
import time


def es_potencia_de_dos(numero):
    # Un número es una potencia de 2 si y solo si tiene un solo bit establecido en su representación binaria.
    # Por lo tanto, verificar si el número es mayor que 0 y su operación "y" lógica con su número menos 1 es igual a 0.
    return numero > 0 and (numero & (numero - 1)) == 0
#print(read_index(1)) #solo es una prueba

def isFull(index:dict, len1: int, len2:int) -> bool: #evalua si un dict se llenó (considerando longitud de los que dict's que se hacen merge)
    current_len: int = len(json.dumps(index).encode('utf-8'))
    return current_len>=len1 or len>=len2
    #return len(json.dumps(index).encode('utf-8'))>=len1 or len(json.dumps(index).encode('utf-8'))>=len2


def BasicMerge(index1:int, index2:int, ruta_origen:str, ruta_destino:str) -> None: #lo unico que hace es escribir
    posting1 = read_index(index1,ruta_origen)
    posting2 = read_index(index2,ruta_origen)
    
    # se calcula tamaño de cada posting
    len1 = len(json.dumps(posting1).encode('utf-8'))
    len2 = len(json.dumps(posting2).encode('utf-8'))

    """
    print("posting1: ",posting1)
    print("posting2: ",posting2)
    print(len1)
    print(len2)

    """

    #para nuevos diccionarios
    result1 = {} 

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
        
        #if result1_full:
        #    print()
            #print("Se completó un bloque", result1)
    
    # sale del bucle, cuando se llena el diccionario "result1"
    write_index(index1,result1,ruta_destino)

    # una vez escrito en memoria, vuelve a definirlo sin elementos
    result1 = {}
         
    # en token1, token2 tengo elementos que aún no añado a ningun bloque resultante

    """ llenado del segundo bloque : la diferencia con este bloque, es que podemos llegar al final y por eso siempre usamos try """
    while True: 
        if token1==token2: #terminos coinciden
            valor1.update(valor2)
            result1[token1] = valor1 #añadimos merge de ambos posting list 
            
            # avanzamos ambos punteros
            try:
                token1, valor1 = next(i1)
                token2, valor2 = next(i2)
            except StopIteration: #se terminó de recorrer un diccionario (no sabemos cuál, pero no es problema)
                break

        elif token1<token2: #añadimos el menor
            result1[token1] = valor1

            try:#intentamos seguir recorriendo el posting1
                token1, valor1 = next(i1)
            except StopIteration:
                break

        else: #añadimos el menor (en este caso, token2)
            result1[token2] = valor2
        
            try: #intentamos seguir recorriendo el posting2
                token2, valor2 = next(i2)
            except StopIteration:
                break
    # para salir del bucle, se debe llegar al final de uno de los diccionarios que se están combinando  

    # añadimos posibles elementos resultantes (del posting1)
    while True:
        try:
            result1[token1] = valor1
            token1, valor1 = next(i1)
        except StopIteration:
            break

    # añadimos posibles elementos resultantes (del posting2)
    while True:
        try:
            result1[token2] = valor2
            token2, valor2 = next(i2)
        except StopIteration:
            break
            

    #print("Bloques finales:")
    #print("Bloque2: ",result1)

    # escribimos bloque final
    write_index(index2,result1,ruta_destino)


"""
for i in range (1,10,2): #prueba con primeros 3 pares de archivos
    BasicMerge(i,i+1)
"""
#MergeBasico(3,4)
#MergeBasico(5,6)

#BasicMerge(1,2)

# merge general (que combina de 4 en 4, 8 en 8, 16 en 16, .... , 2^k en 2^k)
def Merge(index1:int, index2:int, ruta_origen:str, ruta_destino:str) -> None: # index1: extremo izquierdo , index2: extremo derecho 
    # *idea*: verificar rango entre los que se encuentran index1, index2 

    # se define bloques a leer
    nro_bloque_1:int = index1
    final:int = int(index2)
    #print(es_potencia_de_dos(final), "potencia de 2",final)

    
    while not final%2==0:
        final += 1

        
    nro_bloque_2:int = index1 + int((final-index1+1)/2)

    #print("iniciando mitad en :",nro_bloque_2)
    limit:int = nro_bloque_2 # limite para bloque1 

    #print(nro_bloque_1,nro_bloque_2)
    posting1 = read_index(nro_bloque_1,ruta_origen)
    posting2 = read_index(nro_bloque_2,ruta_origen)
    
    # se calcula tamaño de cada posting
    len1 = len(json.dumps(posting1).encode('utf-8'))
    len2 = len(json.dumps(posting2).encode('utf-8'))
    
    contador:int = index1 #para saber en qué bloque escribir el diccionario que se llena

    # iteradores
    i1 = iter(posting1.items())
    i2 = iter(posting2.items())

    # definimos el inicio de cada posting (para empezar a recorrer)
    token1, valor1 = next(i1)
    token2, valor2 = next(i2)

    # para definir qué mitad se llena
    mitad_llena:int = 0

    result = {} #diccionario vacio

    # itera hasta que se llene un bloque o se recorra toda una mitad
    while contador<=index2 and mitad_llena==0: #hace merge desde bloques index1 hasta index2

        isBlockFull:bool = False

        while not isBlockFull and mitad_llena == 0:
            #print(result)
            if token1==token2: #hace merge
                valor1.update(valor2) 
                result[token1] = valor1

                # dos punteros tienen que avanzar
                try:
                    token1, valor1 = next(i1)
                except StopIteration:
                    #print("llegue al final de un bloque de la primera mitad")
                    #aumenta el nro de bloque, lo lee y actualiza longitud
                    nro_bloque_1 += 1

                    if nro_bloque_1==limit: # primera mitad a lo mucho, puede llegar a leer hasta bloque limit-1
                        mitad_llena = 1 
                    else:
                        posting1 = read_index(nro_bloque_1,ruta_origen)
                        len1 = len(json.dumps(posting1).encode('utf-8'))
                        i1 = iter(posting1.items())

                try:
                    token2, valor2 = next(i2)
                except StopIteration:
                    #print("llegue al final de un bloque de la segunda mitad",nro_bloque_2)
                    #aumenta el nro de bloque, lo lee y actualiza longitud
                    nro_bloque_2 += 1

                    if nro_bloque_2>index2: # segunda mitad a lo mucho, puede llegar a leer hasta bloque index2
                        if mitad_llena==0:
                            mitad_llena = 2  # verifica si se llenó otra mitad antes de asignar
                        else:
                            mitad_llena = 1 # si ya se llenó la anterior mitad, dejamos seteado mitad_llena=1
                    else:
                        posting2 = read_index(nro_bloque_2,ruta_origen)
                        #print("leyendo bloque",nro_bloque_2)
                        len2 = len(json.dumps(posting2).encode('utf-8'))
                        i2 = iter(posting2.items())
        
            elif token1<token2:
                result[token1] = valor1

                #avanza iterador 1
                try:
                    token1, valor1 = next(i1)
                except StopIteration:
                    #aumenta el nro de bloque, lo lee y actualiza longitud
                    nro_bloque_1 += 1

                    if nro_bloque_1==limit: # primera mitad a lo mucho, puede llegar a leer hasta bloque limit-1
                        mitad_llena = 1 
                    else:
                        posting1 = read_index(nro_bloque_1,ruta_origen)
                        len1 = len(json.dumps(posting1).encode('utf-8'))
                        i1 = iter(posting1.items())

            else:
                result[token2] = valor2
                
                #avanza iterador 2
                try:
                    token2, valor2 = next(i2)
                except StopIteration:
                    #aumenta el nro de bloque, lo lee y actualiza longitud
                    nro_bloque_2 += 1

                    if nro_bloque_2>index2: # segunda mitad a lo mucho, puede llegar a leer hasta bloque index2
                        mitad_llena = 2 
                    else:
                        posting2 = read_index(nro_bloque_2,ruta_origen)
                        len2 = len(json.dumps(posting2).encode('utf-8'))
                        i2 = iter(posting2.items())
                
            isBlockFull = isFull(result,len1,len2) #verifica si el bloque se llenó

        #print(result)
        #print(isBlockFull)



        if isBlockFull: # escribe el bloque, solo si se llenó
            
            if contador==index2: # por si aun faltan añadir elementos a ultimo bloque
                if token1==token2:
                    valor1.update(valor2)
                    result[token1] = valor1

                    try:
                        token1,valor1 = next(i1)
                    except:
                        mitad_llena = 1 # se recorrió toda primera mitad

                    try:
                        token2, valor2 = next(i2)
                    except:
                        mitad_llena = 2 # se recorrió toda la segunda mitad
                        
            else:
                #print("escribiendo bloque", contador)
                write_index(contador,result,ruta_destino) #escribe el indice (una vez que el puntero se llena)
                #print(result)
                result = {} #diccionario vacio

                # primero escribe en index_contador.json y luego aumenta el contador
                #print(contador) 
                contador+=1  # cada vez que se llena un diccionario se aumenta el contador (así se envía a escribir)
    
    if contador>8 and contador<12:
        print(result, "contador:",contador)
    #print("nro_bloque_2:",nro_bloque_2)
    
    if mitad_llena==1:  # falta escribir elementos de la segunda mitad
        #print("primera mitad está llena")
        isBlockFull = False

        while contador<=index2: 
            while not isBlockFull:
                result[token2] = valor2
                
                #avanza iterador 2
                try:
                    token2, valor2 = next(i2)
                except StopIteration:
                    #aumenta el nro de bloque, lo lee y actualiza longitud
                    nro_bloque_2 += 1
                    #print("here",nro_bloque_2)
                    if nro_bloque_2>index2: # segunda mitad a lo mucho, puede llegar a leer hasta bloque index2
                        write_index(contador,result,ruta_destino) # ya no puede leer mas, solo escribe
                        return None #para finalizar funcion
                        
                    else:
                        #print(nro_bloque_2)
                        posting2 = read_index(nro_bloque_2,ruta_origen)
                        len2 = len(json.dumps(posting2).encode('utf-8'))
                        i2 = iter(posting2.items())
            
                isBlockFull = isFull(result,len2,len2) #verifica si bloque se llenó (solo compara con la longitud de bloque que está añadiendo)
                #print(isBlockFull,end='--')
            
            if isBlockFull: # escribe el bloque, solo si se llenó
                if contador==index2: # por si aun faltan añadir elementos a ultimo bloque
                    while True:
                        try:
                            #print(token2)
                            token2, valor2 = next(i2)
                        except StopIteration:
                            result[token2] = valor2
                            break

                write_index(contador,result,ruta_destino) #escribe el indice (una vez que el puntero se llena)
                result = {} #diccionario vacio

                # primero escribe en index_contador.json y luego aumenta el contador
                #print(contador) 
                contador+=1  # cada vez que se llena un diccionario se aumenta el contador (así se envía a escribir)

   

    elif mitad_llena==2:
        #print("segunda mitad está llena")
        
        
        # falta escribir elementos de la primera mitad
        isBlockFull = False

        while contador<=index2:
            #if contador>8 and contador<12:
                #print(result,"mi contador:",contador)
            while not isBlockFull:
                result[token1] = valor1
                #print("append",token1)
                
                #avanza iterador 1
                try:
                    token1, valor1 = next(i1)
                except StopIteration:
                    #aumenta el nro de bloque, lo lee y actualiza longitud
                    nro_bloque_1 += 1

                    
                    if nro_bloque_1>index2: # segunda mitad a lo mucho, puede llegar a leer hasta bloque index2
                        write_index(contador,result,ruta_destino) #ya no puede leer mas, solo escribe
                        return None # para finalizar funcion
                    else:
                        posting1 = read_index(nro_bloque_1,ruta_origen)
                        len1 = len(json.dumps(posting1).encode('utf-8'))
                        i1 = iter(posting1.items())
                
                isBlockFull = isFull(result,len1,len1) #verifica si bloque se llenó (solo compara con la longitud de bloque que está añadiendo)
            
            if isBlockFull: # escribe el bloque, solo si se llenó

                if contador==index2: # por si aun faltan añadir elementos a ultimo bloque
                    while True:
                        try:
                            #print(token1)
                            token1, valor1 = next(i1)
                        except StopIteration:
                            result[token1] = valor1
                            break

                write_index(contador,result,ruta_destino) #escribe el indice (una vez que el puntero se llena)
                result = {} #diccionario vacio

                # primero escribe en index_contador.json y luego aumenta el contador
                #print(contador) 
                contador+=1  # cada vez que se llena un diccionario se aumenta el contador (así se envía a escribir)

    else:
        print("no llené ninguna mitad")
        
    
#Merge(1,4)
#Merge(33,64)

# ejemplos de llamada a Merge
#Merge(1,8) #combina los 8 primeros bloques (para esto ya se deben haber ordenado de 4 en 4 y de 2 en dos - previamente )
#Merge(9,16) #combina los bloques del 9 al 16 (para esto ya se deben haber ordenado de 4 en 4 y de 2 en dos - previamente )

"""
    Merge siempre se llama así -> Merge(2^k+1, 2^i)
    - Llamadas para bloques de 2 en 2:
        .Merge(1,2)
        .Merge(3,4)
        .Merge(5,6)
        .Merge(7,8)
    - Llamadas para bloques de 4 en 4:
        .Merge(1,4)
        .Merge(5,8)
    - Llamadas para bloques de 8 en 8:
        .Merge(1,8)

    ### Cómo hacer si no tenemos un nro de bloques potencia de 2?
        - Ejemplo - 14 bloques:
            Llamadas para bloques de 2 en 2:
                . Merge(1,2)
                . Merge(3,4)
                . Merge(5,6)
                . Merge(7,8)
                . Merge(9,10)
                . Merge(11,12)
                . Merge(13,14) 
            Llamadas para bloques de 4 en 4:
                . Merge(1,4)
                . Merge(5,8)
                . Merge(9,12)
                . Merge(13,14)? --> NO!, ya está ordenado (si fueran 15?)
            Llamadas para bloques de 8 en 8:
                . Merge(1,8)
                . Merge(9,14) --> SÍ!, hay que ordenar (pero cómo?)
            Llamadas para bloques de 16 en 16:
                . Merge(1,14) --> SÍ, hay que ordenar (pero cómo?)

"""


"""
BasicMerge(1,2,"Initial\\","Merge2\\")
BasicMerge(3,4,"Initial\\","Merge2\\")
BasicMerge(5,6,"Initial\\","Merge2\\")
BasicMerge(7,8,"Initial\\","Merge2\\")

"""

"""
BasicMerge(1,2,"Initial\\","Merge2\\")
BasicMerge(3,4,"Initial\\","Merge2\\")
BasicMerge(5,6,"Initial\\","Merge2\\")
BasicMerge(7,8,"Initial\\","Merge2\\")
"""


"""
for i in range(1,17,2):
    BasicMerge(i,i+1,"Initial\\","Merge2\\")
"""


"""
for i in range(1,17,4):
    Merge(i,i+3,"Merge2\\","Merge4\\")
"""

#Merge(9,12,"Merge2\\","Merge4\\")

"""
for i in range(1,17,8):
    Merge(i,i+7,"Merge4\\","Merge8\\")
"""
"""
Merge(1,4,"Merge2\\","Merge4\\")
Merge(5,8,"Merge2\\","Merge4\\")
"""

"""
Merge(1,8,"Merge4\\","Merge8\\")
"""

#BasicMerge(1,2,"Initial\\","Merge2\\")
#Merge(1,3,"Merge2\\","Merge4\\")
#BasicMerge(5,8,"Initial\\","Merge2\\")

#Merge(1,3,"Merge2\\","Merge4\\")


block = 532
for i in range (1,block,8):
    if i+7<=block:
        Merge(i,i+7,"Merge4\\","Merge8\\")
	#BasicMerge(i,i+7,"Merge4\\","Merge8\\")