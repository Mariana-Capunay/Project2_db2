import json
import time
# Ruta al archivo CSV
archivo_csv = r"C:\Users\ASUS\Downloads\prueba\styles.csv"
#archivo_csv = ruta_archivo = r"C:\Users\HP\Desktop\styles\styles.csv" # Ruta del archivo CSV

# Posición específica en bytes donde se encuentra la línea que deseas leer
#posicion_bytes = 4376342  # Por ejemplo, la posición 100 en el archivo
#posicion_bytes = 1211484


"""tamaño de primera linea es 97, pero para leer la segunda -> pos_row = 98"""
#posicion_bytes = 98+93+1  # Por ejemplo, la posición 100 en el archivo
def get_row(posicion_bytes):
    # Abre el archivo en modo lectura en binario
    with open(archivo_csv, 'rb') as archivo:
        # Posiciona el puntero del archivo en la posición específica
        archivo.seek(int(posicion_bytes))

        # Lee la línea en la posición específica
        linea_especifica = archivo.readline()

        # Convierte los bytes a cadena (decodificación utf-8)
        linea_especifica = linea_especifica.decode('utf-8')

        return linea_especifica
        # Imprime la línea específica
        #print(f'Linea en la posicion {posicion_bytes} bytes: {linea_especifica}')


# with open("normas.json","r") as archivo: #abre archivo de normas
#     diccionario_normas = json.load(archivo)

    
#     with open(archivo_csv, 'rb') as archivo_csv: #abre csv (para leer cada fila)
#         i = 0
#         for pos_fila in diccionario_normas:
#             archivo_csv.seek(int(pos_fila)) #vamos a la posicion de fila que indica
#             print(archivo_csv.readline().decode('utf-8')) #imprimimos una linea
#             i+=1
#             if i==20:
#                 time.sleep(3)
#                 i=0


        