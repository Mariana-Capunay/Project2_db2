from read_index import read_index #importamos funcion para leer un bloque de indice especifico

print(read_index(1))

def MergeBasico(index1:int, index2:int) -> None: #lo unico que hace es escribir
    posting1 = read_index(index1)
    posting2 = read_index(index2)
    print("")



