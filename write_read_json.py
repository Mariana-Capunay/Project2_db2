import json

# Conjunto de diccionarios que deseas escribir en el archivo
conjunto_de_diccionarios = [
    {"nombre": "Ejemplo1", "edad": 30},
    {"nombre": "Ejemplo2", "edad": 35},
    {"nombre": "Ejemplo3", "edad": 40}
]

# Escribir el conjunto de diccionarios en un archivo JSON
with open("conjunto_de_diccionarios.json", "w") as archivo:
    json.dump(conjunto_de_diccionarios, archivo)


# Leer el conjunto de diccionarios desde el archivo JSON
with open("conjunto_de_diccionarios.json", "r") as archivo:
    conjunto_leido = json.load(archivo)

# Imprimir el conjunto de diccionarios leído
print(conjunto_leido)
