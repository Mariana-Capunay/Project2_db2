index1 = [1,3,5,7] #de termID's
index2 = [2,4,6,8] #de termID's


def is_full(lista:dict) -> bool: #funcion basica para verificar si esta lleno (en este caso)
    return len(lista)>=4


"""
    1. Usar dos punteros a termID, uno para cada index
    2. Si los valores de los punteros son iguales
        a. Mezclar ambas listas y agregar al nuevo bloque
    3. Caso contrario
        a. Agregar la lista del menor termID al nuevo bloque y avanzar dicho puntero
        b. Regresar al paso 2
    4. Si el nuevo bloque se llena, crear otro bloque y continuar con el proceso hasta que ambos punteros llegan al final del índice
"""

def Merge1(index1:dict, index2:dict):
    r1 = [] #para guardar bloques resultantes
    r2 = []
    i1 = i2 = 0
    r1_full = r2_full = False

    while not r1_full:
        if index1[i1]==index2[i2]:
            r1.append(index1[i1])
            i1+= 1
            i2+= 1
        elif index1[i1]<index2[i2]:
            r1.append(index1[i1])
            i1+=1
        else:
            r1.append(index2[i2])            
            i2+=1

        r1_full = is_full(r1) 
        if r1_full:
            print("Se completó un bloque", r1)
            


    while i1<len(index1) and i2<len(index2) and not is_full(r2):
        if index1[i1]==index2[i2]:
            r2.append(index1[i1])
            i1+= 1
            i2+= 1
        elif index1[i1]<index2[i2]:
            r2.append(index1[i1])
            i1+=1
        else:
            r2.append(index2[i2])            
            i2+=1

        r2_full = is_full(r2)
        if r2_full:
            print("Se completó un bloque", r2)

    # añadimos posibles elementos resultantes
    while i1<len(index1):
        r2.append(index1[i1])
        i1+= 1

    while i2<len(index2):
        r2.append(index2[i2])
        i2+= 1

    print("Bloques finales:",r1,r2)

Merge1(index1=index1, index2=index2)


