import os

# Ruta al directorio donde se encuentran los archivos JSON
directorio = r"C:\Users\ASUS\OneDrive - UNIVERSIDAD DE INGENIERIA Y TECNOLOGIA\Escritorio\bd2_proyecto_2023.2\proyecto_2\Project2_db2\InvertedIndex\Local_Index\Merge128"
#directorio = r"C:\Users\HP\Desktop\UTEC\Ciclo_VI\Base_de_datos_II\Proyecto_2\Project2_db2\InvertedIndex\Local_Index"

# Lista todos los archivos en el directorio
archivos = os.listdir(directorio)

# Itera sobre los archivos y elimina los que contienen "index" en su nombre
for archivo in archivos:
    if archivo.endswith('.json') and 'index' in archivo:
        ruta_completa = os.path.join(directorio, archivo)
        # Elimina el archivo
        os.remove(ruta_completa)
        print(f'Archivo eliminado: {ruta_completa}')

print('Proceso completado.')
