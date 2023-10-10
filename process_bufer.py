import time

# Tamaño máximo del buffer en bytes
tamaño_maximo_buffer = 4096  # Puedes ajustar este valor según tus necesidades

# Ruta del archivo que deseas leer
ruta_archivo = r"C:\Users\ASUS\Downloads\prueba\styles.csv"

# Abrir el archivo en modo lectura
with open(ruta_archivo, "r", encoding="utf-8") as archivo:
    while True:
        buffer = []  # Lista para almacenar las líneas del buffer
        tamaño_buffer = 0  # Tamaño actual del buffer
        
        # Leer líneas del archivo y agregarlas al buffer hasta que el tamaño máximo se alcance
        for linea in archivo:
            tamaño_linea = len(linea.encode("utf-8"))  # Tamaño de la línea en bytes
            # Si la línea cabe en el buffer sin exceder el tamaño máximo
            if tamaño_buffer + tamaño_linea <= tamaño_maximo_buffer:
                buffer.append(linea.strip())  # Agrega la línea al buffer
                tamaño_buffer += tamaño_linea  # Actualiza el tamaño del buffer
            else:
                break  # Si excede el tamaño máximo, detén la lectura del buffer
        
        # Procesar el buffer (hacer lo que necesites con las líneas leídas)
        print("Nuevo buffer:\n\n", "\n".join(buffer))  # En este ejemplo, simplemente imprime el buffer
        print("Tamaño buffer: ",tamaño_buffer)
        # Pausa el programa por 3 segundos antes de leer el siguiente buffer
        time.sleep(3)
        
        # Si el archivo ha llegado al final, sal del bucle
        if not buffer:
            break
