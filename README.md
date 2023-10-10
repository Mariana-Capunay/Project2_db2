# Project2_db2
# Idea
1. Leer el .csv de acuerdo a cantidad de un buffer (considerando que tome nro exacto de filas - no haga particion)
2. Concatenar datos de cada fila (preguntar acerca de ponderacion)
3. Formar un hash para cada bloque
4. Generar un posting_list -> [(docid, tf),...]  - como indice invertido
5. Una vez se completa pasos del 1 al 4, enviar el diccionario a disco
6. Ordena los terminos del diccionario
7. Escribe el indice invertido (del buffer - local) en disco
8. Repetir pasos del 1 al 7 por cada buffer
9. Retornar nombre de archivo en el que está cada buffer
10. Hacer Merge con todos los buckets  (mezcla en big Index)

# Query Idea
1. Obtiene indice invertido de la query
2. Extrae indice invertido (general)
3. Aplica similitud coseno (no es necesario crear vectores de mismo espacio, hay que aprovechar uso de diccionarios para guardar cada termino)

