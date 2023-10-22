import json
import sys 
sys.path.append('../')
from rutas import ruta_indices


def read_json(nombre_archivo:str)->dict:
    with open(ruta_indices+"/"+nombre_archivo,'r') as archivo:
        result = json.load(archivo)
    return result

print(read_json("index01.json"))
