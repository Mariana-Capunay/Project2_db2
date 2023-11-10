import json
import io
tamaño_maximo_buffer = io.DEFAULT_BUFFER_SIZE

ruta_indices = r"C:\Users\ASUS\OneDrive - UNIVERSIDAD DE INGENIERIA Y TECNOLOGIA\Escritorio\bd2_proyecto_2023.2\proyecto_2\Project2_db2\InvertedIndex\Local_Index"

#ruta_indices = r"C:\Users\HP\Desktop\UTEC\Ciclo_VI\Base_de_datos_II\Proyecto_2\Project2_db2\InvertedIndex\Local_Index"
#ruta_indices = r"C:\Users\HP\Desktop\UTEC\Ciclo_VI\Base_de_datos_II\Proyecto_2\Project2_db2\InvertedIndex\test_index"

def read_json(nombre_archivo:str)->dict:
  # try:
    with open(ruta_indices+ "\\" + nombre_archivo,'r') as archivo:
        result = json.load(archivo)
    return result
    #except FileNotFoundError:
     #   return {}

def read_index(nro_index:int, ruta:str="")->dict:
    nro_index_str:str = str(nro_index) #convierte el nro de index a string

    if nro_index<10: #caso en el que se debe añadir un cero al inicio
        nro_index_str = "0"+nro_index_str
    return read_json(ruta+"index"+nro_index_str+".json")

#print(json.dumps(read_index(2,"Initial")))
# for i in range (1,15):
#     d1 = len(json.dumps(read_index(i,"Merge8\\")).encode('utf-8'))
#     print(i,"->",d1)
#d2 = len(json.dumps(read_index(16)).encode('utf-8'))
#print(d2)
"""casos de prueba"""
#print("Indice 1:", read_index(1))
#print("Indice 2:", read_index(2))


