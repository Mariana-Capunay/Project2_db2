import pandas as pd
import numpy as np
import glob

path_base = r"C:\Users\ASUS\Downloads\prueba" #carpeta en la que almacenamos archivo csv 

#archivo_original = pd.read_csv(path_base+"\styles.csv")

import pandas as pd

# Lee las primeras 9 columnas de forma normal
primeras_columnas = pd.read_csv(path_base+"\styles.csv", usecols=range(9))

# Lee el texto después de las primeras 9 columnas como una sola columna
texto_adicional = pd.read_csv(path_base+"\styles.csv", usecols=[9])

# Combina los DataFrames en uno solo
df_completo = pd.concat([primeras_columnas, texto_adicional], axis=1)

# Muestra las primeras filas del DataFrame resultante
print(path_base) #ruta
print(len(df_completo))

partes = np.array_split(df_completo, 32) #parte contenido en 20 DataFrames (bloques)
print(partes)

for ix, df in enumerate(partes):
   df.to_csv(path_base+"\prueba"+str(ix+1).zfill(2)+".csv", index=False) #completa con dos ceros (zfill)
    #df.to_excel(path_base+"\prueba"+str(ix+1).zfill(2)+".xlsx", index=False) #completa con dos ceros (zfill)

#para hallar todas las rutas
rutas = glob.glob(path_base+"\prueba*.csv")
print(rutas)

partes_glob = [pd.read_csv(ruta) for ruta in rutas]


archivo_completo = pd.concat(partes_glob) #unifica a todos los archivos leidos (solo porque tienen la misma estructura)
    # Columnas no coincidentes -> se completan con Nan