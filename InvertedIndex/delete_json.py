import os

# Ruta al directorio donde se encuentran los archivos JSON
directorio = r"C:\Users\ASUS\OneDrive - UNIVERSIDAD DE INGENIERIA Y TECNOLOGIA\Escritorio\bd2_proyecto_2023.2\proyecto_2\Project2_db2\InvertedIndex\Local_Index"
#directorio = r"C:\Users\HP\Desktop\UTEC\Ciclo_VI\Base_de_datos_II\Proyecto_2\Project2_db2\InvertedIndex\Local_Index"

def remove_jsons(ruta):
    
    # Lista todos los archivos en el directorio
    archivos = os.listdir(ruta)
    
    # Itera sobre los archivos y elimina los que contienen "index" en su nombre
    for archivo in archivos:
        if archivo.endswith('.json') and 'index' in archivo:
            ruta_completa = os.path.join(ruta, archivo)
            # Elimina el archivo
            os.remove(ruta_completa)
            print(f'Archivo eliminado: {ruta_completa}')

    print('Proceso completado para el directorio',ruta)


remove_jsons(directorio+"\\Initial\\")
remove_jsons(directorio+"\\Merge2\\")
remove_jsons(directorio+"\\Merge4\\")
remove_jsons(directorio+"\\Merge8\\")
remove_jsons(directorio+"\\Merge16\\")
remove_jsons(directorio+"\\Merge32\\")
remove_jsons(directorio+"\\Merge64\\")
remove_jsons(directorio+"\\Merge128\\") #en esta carpeta, está el indice global