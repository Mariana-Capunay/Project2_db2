# Ruta al archivo CSV
#archivo_csv = r"C:\Users\ASUS\Downloads\prueba\styles.csv"
archivo_csv = r"C:\Users\HP\Desktop\styles\styles.csv"

# Abre el archivo CSV en modo lectura
with open(archivo_csv, 'r') as archivo:
    # Lee la primera línea (encabezados) y la almacena en una variable (opcional)
    encabezados = archivo.readline().strip().split(',')
    print('Encabezados del CSV:', encabezados)
    i = 0
    # Itera a través de las líneas restantes del archivo CSV
    for linea in archivo:
        # Procesa cada línea como una lista de valores
        valores = linea.strip().split(',')
        print('Valores procesados:', valores)
        i+=1
        if i==3:
            break;
