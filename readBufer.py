import csv
import itertools

# Especifica el número de líneas por página que deseas leer
lineas_por_pagina = 100  # Cambia esto según tus necesidades

# Abre el archivo CSV en modo lectura
with open(r"C:\Users\ASUS\Downloads\prueba\styles.csv", 'r') as archivo_csv:
    # Lee 4096 bytes desde el archivo
    datos = archivo_csv.read(4096)
    # Imprime los datos leídos
    print(datos)