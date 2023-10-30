# Búsqueda y recuperación de la información
## Organización del equipo
| Participante | Papel |
|--------------|--------------|
| Mariana Capuñay   | Procesamiento del CSV-Creación de índice invertido, Manejo de índices, Implementación de SPIMI, Merge |
| Manyory Cueva    | Frontend, Ponderación de pesos en postgresql  | 
| Jaime Ramos    |  Creación del índice invertido, Análisis de normas por fila, Conexión con postgresql, Análisis de SPIMI, Merge | 
| Gustavo Orosco  |  | 

## Table of Contents  
### Introducción
1. [Descripción del dominio de datos](#id1)
2. [Librerías utilizadas](#id2)
3. [Técnica de indexación de las librerías utilizadas](#id3)
4. [Como se realiza el KNN Search y el Range Search](#id4)
### Backend
5. [Construcción del índice invertido](#id5)
   ![image](https://github.com/Mariana-Capunay/Project2_db2/assets/91238621/d55a5a16-7552-4dd7-95ac-cb1bef9c9975)


7. [Manejo de memoria secundaria](#id6)
8. [Ejecución óptima de consultas](#id7)
### Análisis de la maldición de la dimensionalidad y como mitigarlo
### Frontend
8. [Diseño del índice con PostgreSQL/MongoDB](#id8)
9. [Análisis comparativo con su propia implementación](#id9)
10. [Screenshots de la GUI](#id10)
## Experimentación
11. [Tablas y gráficos de los resultados](#id11)
12. [Análisis y discusión](#id12)


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
    
# Json to Csv
Por temas de facilidad y actualización de funciones considerando la longitud variable  usaremos en el manejo de la data archivos json.

# Query Idea
1. Obtiene indice invertido de la query
2. Extrae indice invertido (general)
3. Aplica similitud coseno (no es necesario crear vectores de mismo espacio, hay que aprovechar uso de diccionarios para guardar cada termino)

# Para obtener posición de una fila
pos_row = tamaño de bytes leídos + 1
- pos_row de encabezado = 0
- pos_row de primera fila = pos_row(luego de encabezado) + tamaño de encabezado + len('\n') = 0+97+1
- pos_row de segunda fila = bytes antes de primera fila + tamaño de primera fila + len('\n') = 98 +93+1
