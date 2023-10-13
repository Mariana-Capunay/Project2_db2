import linecache
# Número de la línea específica que quieres leer
numero_de_linea = 2  # Por ejemplo, la línea número 2

# Ruta al archivo CSV
archivo_csv = r"C:\Users\ASUS\Downloads\prueba\styles.csv"

# Lee la línea específica del archivo CSV
linea_especifica = linecache.getline(archivo_csv, numero_de_linea)

# Imprime la línea específica
print(f'Línea {numero_de_linea}: {linea_especifica}')