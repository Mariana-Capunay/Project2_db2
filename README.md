# Búsqueda y recuperación de la información
## Organización del equipo
| Participante | Papel |
|--------------|--------------|
| Mariana Capuñay   | Procesamiento del CSV-Creación de índice invertido, Manejo de índices, Implementación de SPIMI, Merge |
| Manyory Cueva    | Frontend, Ponderación de pesos en postgresql, cosine  | 
| Jaime Ramos    |  Creación del índice invertido, Análisis de normas por fila, Conexión con postgresql, Análisis de SPIMI, Merge | 
| Gustavo Orosco  |  | 

# Tabla de contenidos 
## Introducción
1. [Descripción del dominio de datos](#id1)
2. [Librerías utilizadas](#id2)
3. [Técnica de indexación de las librerías utilizadas](#id3)
4. [Como se realiza el KNN Search y el Range Search](#id4)
## Backend
5. [Construcción del índice invertido](#id5)
6. [Manejo de memoria secundaria](#id6)
7. [Ejecución óptima de consultas](#id7)
## Maldición de la dimensionalidad
8. [Análisis de la maldición de la dimensionalidad y cómo mitigarlo](#id8)

## Frontend
9. [Diseño del índice con PostgreSQL/MongoDB](#id9)
10. [Análisis comparativo con su propia implementación](#id10)
11. [Screenshots de la GUI](#id11)
## Experimentación
12. [Tablas y gráficos de los resultados](#id12)
13. [Análisis y discusión](#id13)
----------------------------------------------

## Descripción del dominio de datos<a name="id1"></a>
Fashion Products Dataset, es una recopilación estructurada de información sobre productos de moda. Esta información se separa en dos archivos principales **.csv**:
<div style="text-align:center">
    <img src="images/fashion-products-dataset.jpg" alt="Fashion Products" width="200" height="200">
</div>

- **styles.csv**: Este archivo contiene las columnas *id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName*. La información de cada producto es representada en una fila:
<div style="text-align:center">
    <img src="images/styles_csv.png" alt="Primeras filas de styles.csv" width="400" height="190">
</div>

- **images.csv**: Este archivo contiene las columnas *filename,link*, donde 
  - *filename* representa el id de cada imagen 
  - *link* representa la ubicación de cada imagen
<div style="text-align:center">
    <img src="images/images_csv.png" alt="Primeras filas de images.csv" width="400" height="150">
</div>

----------------------------------------------
## Librerías utilizadas<a name="id2"></a>
### Para el índice invertido
  - **nltk** : hacemos uso de la función *nltk.word_tokenize()* para el preprocesamiento. 
  <div style="text-align:center">
    <img src="images/uso_nltk_1.png" alt="Importanto módulos" width="300" height="35">
</div>
  <div style="text-align:center">
    <img src="images/uso_nltk_2.png" alt="Uso de nltk.word_tokenize()" width="300" height="45">
</div>

  También importamos el módulo *nltk.stem.snowball* para posteriormente usarlo con el método *SnowballStemmer('english')* y *stem*, lo cual nos permite reducir las palabras a su forma base o raíz (lexema)
    <div style="text-align:center">
    <img src="images/uso_nltk_3.png" alt="Uso de SnowballStemmer('english')" width="300" height="45">
  </div>
    <div style="text-align:center">
    <img src="images/uso_nltk_4.png" alt="Uso de stemmer.stem()" width="300" height="25">
  </div>


  - **os** : hacemos uso de la función *os.path.getsize()*, la cual nos permite obtener el tamaño, en bytes, de un archivo especifico
  <div style="text-align:center">
    <img src="images/uso_de_os_1.png" alt="Uso de os.path.getsize()" width="300" height="32">
  </div>
  
  - **io** : hacemos uso de la función *io.DEFAULT_BUFFER_SIZE*, la cual representa el tamaño predeterminado del búfer utilizado por las operaciones de entrada/salida
  <div style="text-align:center">
    <img src="images/uso_de_io_1.png" alt="Uso de io.DEFAULT_BUFFER_SIZE" width="300" height="45">
  </div>

  - **json** : para manejar la creación y lectura de los posting list en disco
  <div style="text-align:center">
    <img src="images/uso_de_json_1.png" alt="Uso de json.dump(normas,archivo)" width="300" height="50">
  </div>
  <div style="text-align:center">
    <img src="images/uso_de_json_2.png" alt="Uso de json.dump(indice_local,archivo)" width="300" height="72">
  </div>

  Adicionalmente, también hemos definido funciones que gestionan la lectura y escritura de un archivo **index+nro.json**
  <div style="text-align:center">
    <img src="images/uso_de_json_3.png" alt="Uso de json para read_json y read_index" width="400" height="163">
  </div>
  <div style="text-align:center">
    <img src="images/uso_de_json_4.png" alt="Uso de json para write_json y write_index" width="400" height="178">
  </div>
  

  - **math** : Usamos los métodos _pow_ y _sqrt_ para el cálculo de la norma por fila
    <div style="text-align:center">
    <img src="images/uso_de_math_1.png" alt="Uso de json para read_json y read_index" width="300" height="20">
  </div>
  <div style="text-align:center">
    <img src="images/uso_de_math_2.png" alt="Uso de json para write_json y write_index" width="300" height="30">
  </div>

### Para el índice multimedia
### Para el frontend

----------------------------------------------
## Construcción del índice invertido<a name="id5"></a>
  ![norma](images/norrma.jpg)
  ![poting](images/posting_list.jpg)
  ![binary](images/binary_search.jpg)
  ![creacion](images/crearcion_de_valor.jpg)
  ![apimi](images/merge_spimi.jpg)

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
