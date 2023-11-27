# Búsqueda y recuperación de la información
## Organización del equipo
| Participante | Papel |
|--------------|--------------|
| Mariana Capuñay   | Procesamiento del CSV-Creación de índice invertido, Manejo de índices, Implementación de SPIMI, Merge, cosine |
| Manyory Cueva    | Frontend, Ponderación de pesos en postgresql, cosine  | 
| Jaime Ramos    |  Creación del índice invertido, Análisis de normas por fila, Conexión con postgresql, Análisis de SPIMI, Merge | 
| Gustavo Orosco  | Binary search para buscar palabras, Generación de vectores caracteristicos e indices para registros de longitud variable, KNN secuencial | 

# Tabla de contenidos 
## Introducción
1. [Descripción del dominio de datos](#id1)
2. [Librerías utilizadas](#id2)
3. [Técnica de indexación de las librerías utilizadas - Indice multimedia](#id3)
4. [Como se realiza el KNN Search y el Range Search](#id4)
## Backend
5. [Construcción del índice invertido](#id5)
6. [Manejo de memoria secundaria](#id6)
7. [Ejecución óptima de consultas](#id7)
## Maldición de la dimensionalidad
8. [Análisis de la maldición de la dimensionalidad y cómo mitigarlo](#id8)

## Frontend
9. [Diseño del índice con PostgreSQL](#id9)
10. [Análisis comparativo con su propia implementación](#id10)
11. [Screenshots de la GUI](#id11)
## Experimentación
12. [Resultados de la query](#id12)
13. [Análisis y discusión](#id13)
----------------------------------------------

## 1. Descripción del dominio de datos<a name="id1"></a>
Fashion Products Dataset, es una recopilación estructurada de información sobre productos de moda. Esta información se separa en dos archivos principales **.csv**:
<p align="center">
    <img src="images/fashion-products-dataset.jpg" alt="Fashion Products" width="400">
</p>

- **styles.csv**: Este archivo contiene las columnas *id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName*. La información de cada producto es representada en una fila:
<p align="center">
    <img src="images/styles_csv.png" alt="Primeras filas de styles.csv" width="700" height="">
</p>

- **images.csv**: Este archivo contiene las columnas *filename,link*, donde 
  - *filename* representa el id de cada imagen 
  - *link* representa la ubicación de cada imagen
<p align="center">
    <img src="images/images_csv.png" alt="Primeras filas de images.csv" width="700" height="">
</p>

----------------------------------------------
## 2. Librerías utilizadas<a name="id2"></a>
### 2.1 Para el índice invertido
  - **nltk** : hacemos uso de la función *nltk.word_tokenize()* para el preprocesamiento. 
  <p align="center">
    <img src="images/uso_nltk_1.png" alt="Importanto módulos" width="500" height="">
  </p>
  <p align="center">
    <img src="images/uso_nltk_2.png" alt="Uso de nltk.word_tokenize()" width="500" height="">
  </p>

  También importamos el módulo *nltk.stem.snowball* para posteriormente usarlo con el método *SnowballStemmer('english')* y *stem*, lo cual nos permite reducir las palabras a su forma base o raíz (lexema)
    <p align="center">
    <img src="images/uso_nltk_3.png" alt="Uso de SnowballStemmer('english')" width="500" height="">
    </p>
    <p align="center">
    <img src="images/uso_nltk_4.png" alt="Uso de stemmer.stem()" width="500" height="">
    </p>


  - **os** : hacemos uso de la función *os.path.getsize()*, la cual nos permite obtener el tamaño, en bytes, de un archivo especifico
  <p align="center">
    <img src="images/uso_de_os_1.png" alt="Uso de os.path.getsize()" width="500" height="">
  </p>
  
  - **io** : hacemos uso de la función *io.DEFAULT_BUFFER_SIZE*, la cual representa el tamaño predeterminado del búfer utilizado por las operaciones de entrada/salida
  <p align="center">
    <img src="images/uso_de_io_1.png" alt="Uso de io.DEFAULT_BUFFER_SIZE" width="500" height="">
  </p>

  - **json** : para manejar la creación y lectura de los posting list en disco
  <p align="center">
    <img src="images/uso_de_json_1.png" alt="Uso de json.dump(normas,archivo)" width="500" height="">
  </p>
  <p align="center">
    <img src="images/uso_de_json_2.png" alt="Uso de json.dump(indice_local,archivo)" width="500" height="">
  </p>

  Adicionalmente, también hemos definido funciones que gestionan la lectura y escritura de un archivo **index+nro.json**
  <p align="center">
    <img src="images/uso_de_json_3.png" alt="Uso de json para read_json y read_index" width="500" height="">
  </p>
  <p align="center">
    <img src="images/uso_de_json_4.png" alt="Uso de json para write_json y write_index" width="500" height="">
  </p>

  - **math** : Usamos los métodos _log10_ y _sqrt_ para el cálculo de la norma por fila
  <p align="center">
    <img src="images/uso_de_math_1.png" alt="Uso de math.log10()" width="500" height="">
  </p>
  <p align="center">
    <img src="images/uso_de_math_2.png" alt="Uso de math.sqrt()" width="500" height="">
  </p>

  - **csv** : para obtener rápidamente cada fila del csv al construir la tabla en PostgreSQL. 
  <p align="center">
    <img src="images\csv_init.PNG" alt="Lectura de archivo con csv" width="400" height="">
  </p>

  - **psycopg2** : permite establecer la conexión con la base de datos en postgreSQL, así como ejecutar comandos desde Python y obtener sus outputs.
  <p align="center">
    <img src="images\connection.PNG" alt="Uso de psycopg2" width="350" height="">
  </p>

### 2.2 Para el índice multimedia
### 2.3 Para el frontend
  - **flask** : 


----------------------------------------------

## 3. Técnica de indexación de las librerías utilizadas - Indice multimedia <a name="id3"></a>


----------------------------------------------

## 4. Como se realiza el KNN Search y el Range Search <a name="id4"></a>

----------------------------------------------

## 5. Construcción del índice invertido<a name="id5"></a>
El dataset trabajado en este proyecto no puede manejarse en memoria RAM, por tal motivo hemos optado por una solución escalable que tome en cuenta las consideraciones de hardware: memoria, disco, velocidad.

Por temas de facilidad (considerando la longitud variable)manejaremos los diccionarios de la data archivos *.json*.

Nuestra implementación se basa en el algoritmo SPIMI (Single Pass In-Memory Indexing), el cual es utilizado para la construcción eficiente de índices invertidos.
  <p align="center">
    <img src="images/algorithm_spimi.jpg" alt="Algoritmo SPIMI" width="500" height="">
  </p>

  Nuestra implementación consiste en:
  1. Leer el archivo .csv de acuerdo a cantidad de un buffer (considerando que tome nro exacto de filas, es decir, no haga particion de filas)
  2. Preprocesar cada fila
  3. Concatenar datos de cada fila (calculando la norma y el peso de cada palabra por fila)
  <p align="center">
    <img src="images/norma.jpg" alt="Cálculo de norma-Indice invertido" width="500" height="">
  </p>

  - Para calcular el valor-peso de una palabra en una fila, consideramos su frecuencia en cada campo y multiplicamos  (frecuencia de palabra en el campo*peso del campo)
  <p align="center">
    <img src="images/creacion_de_valor.jpg" alt="Cálculo de valor por palabra-Indice invertido" width="800" height="">
  </p>

  4. Inicializar un hash (diccionario) para cada bloque: este diccionario contendrá
  - palabra: {pos_fila, peso de palabra para esa fila}
  - por palabra: solo se guardará las posiciones de filas en las que la palabra tiene un peso mayor a 0

  5. Completar el diccionario con todas las palabras preprocesadas del bloque
  <p align="center">
    <img src="images/block_dictionary.png" alt="Diccionario local" width="500" height="">
  </p>

  6. Enviar el diccionario local (del buffer) a disco
  <p align="center">
    <img src="images/posting.jpg" alt="Posting List local-Indice invertido" width="800" height="">
  </p>

  7. Repetir pasos del 1 al 6 por cada buffer
  8. Una vez que se termine de preprocesar todos los bloques del .csv, hacer Merge entre los índices locales (mezcla en big Index)
  <p align="center">
    <img src="images/merge_1.jpg" alt="Merge local index into global index" width="800" height="">
    <img src="images/merge_2.jpg" alt="Merge local index into global index_" width="800" height="">
  </p>

  9. Una vez terminado el paso 8, se tiene un solo índice global distribuido entre todos los archivos de índice (.json)

### Para obtener posición de una fila
<p align="center">

$$ pos \space row \space actual = tamaño \space de \space bytes \space leídos $$

</p>

- pos_row de encabezado = 0
- pos_row de primera fila = pos_row(luego de encabezado) + tamaño de encabezado = 0+97 = 97
- pos_row de segunda fila = bytes antes de primera fila + tamaño de primera fila = 98 +92 = 190
----------------------------------------------

## 6. Manejo de memoria secundaria <a name="id6"></a>

Utilizamos el archivo normas.json para almacenar el índice invertido generado. El diccionario almacena la información como [pos_row]:norma.

Luego, para comenzar a crear el índice global, almacenamos cada diccionario local en Local_Index. Al inicio, observamos que el número de diccionarios creados era excesivo (alrededor de 530). Además, encontramos que este número de archivos json perjudicaba la eficiencia de la creación del índice global.

Para ello, incrementamos el tamaño máximo de cada diccionario multiplicando el valor de DEFAULT_BUFFER_SIZE de la librería io por una cantidad que no perjudique la lectura de datos. Con ello, el número de diccionarios se redujo a 128.

<p align="center">
    <img src="images\new_buffer.PNG" alt="Modificadion del buffer" width="600" height="">
  </p>  

Tras este cambio, procedimos a ejecutar el índice global con el algoritmo SPIMI. Para evitar mezclar o perder información en cada iteración, creamos una carpeta por cada iteración hasta el final del algoritmo. Finalmente, para liberar memoria, eliminamos los diccionarios de las carpetas procesadas por el merge excepto por la última, que contiene el índice global completo.

----------------------------------------------

## 7. Ejecución óptima de consultas <a name="id7"></a>
Al recibir una query, lo que se hace es:
1. Obtener el índice invertido de la query
2. Aplicar similitud coseno (no es necesario crear vectores de mismo espacio, se aprovecha uso de diccionarios)

Adicional a ello, cabe recalcar que ya tenemos el índice invertido global de nuestro dataset en disco. Y que estamos haciendo uso de la búsqueda binaria para encontrar un término y sus ocurrencias:
  <p align="center">
    <img src="images/binary_search.jpg" alt="Búsqueda binaria" width="600" height="">
  </p>  

Todo esto facilita el tiempo de las consultas (considerando que el índice invertido global del dataset solo se genera al inicio de nuestro programa y luego no se modifica).

## 8. Análisis de la maldición de la dimensionalidad y cómo mitigarlo <a name="id8"></a>

## 9. Diseño del índice con PostgreSQL <a name="id9"></a>

- Para cargar nuestro dataset en postgress hicimos uso de las librerías *psycopg2* y *csv*.
  <p align="center">
    <img src="images/librerias_sql.png" alt="Uso de psycopg2" width="450" height="">
  </p>  

- Lo primero que hicimos, fue definir la función **init** para crear la tabla *styles* y poblarla con los datos del dataset.
  <p align="center">
    <img src="images/create_table_sql.png" alt="Creando la tabla styles, en caso no exista" width="750" height="">
  </p>  

- Además, dentro de la misma función, añadimos la creación de dos columnas del tipo *weighted_tsv*. Una de estas la indexaremos y será la que usaremos en nuestra búsqueda.
  <p align="center">
    <img src="images/add_vector_sql.png" alt="Creando columnas de tipo weighted_tsv" width="750" height="">
  </p> 

- Luego, definimos la función para retornar las k filas más similares a una query.
  <p align="center">
    <img src="images/searchk_sql.png" alt="Consulta para retornar k más similares" width="750" height="">
  </p> 

  *Al momento de realizar las pruebas notamos que si concatenamos cada palabra de la query con el operador AND ('&') se tiene respuestas más similares que si concatenamos los elementos con OR ('|'). Atribuimos que esto se da porque,  [según la documentación de SQL](https://www.postgresql.org/docs/current/textsearch-controls.html), la versión de búsqueda no considera la rareza de un término.* 



## 10. Análisis comparativo con su propia implementación <a name="id10"></a>

## 11. Screenshots de la GUI <a name="id11"></a>
  - Pantalla principal

  <p align="center">
    <img src="images/mainpage.PNG" alt="Página principal" width="800" height="">
  </p>



## 12. Resultados de la query <a name="id12"></a>
- Aplicamos la query textual *"red shoes"*
  - Resultados con índice invertido
    <p align="center">
      <img src="images/red_shoes_inverted_index.jfif" alt="Página principal" width="800" height="">
    </p>

  - Resultados con postgresSQL
    <p align="center">
      <img src="images/red_shoes_sql.jfif" alt="Página principal" width="800" height="">
    </p>

- Aplicamos la query textual *"green pants"*
  - Resultados con índice invertido
    <p align="center">
      <img src="images/green_pants_inverted_index.jfif" alt="Página principal" width="800" height="">
    </p>

  - Resultados con postgresSQL
    <p align="center">
      <img src="images/green_pants_sql.jfif" alt="Página principal" width="800" height="">
    </p>

## 13. Análisis y discusión <a name="id13"></a>

- Al aplicar las queries textuales y comparar su similitud con los resultados obtenidos en postgresSQL, notamos que nuestra implementación es mucho más óptima al retornar los resultados similares. Sin embargo, postgres proporciona búsquedas más exactas al enviar cada palabra de la query con el operador AND ("&"), pero al usar el operador OR("|") no considera la rareza de los términos, ya que da resultados sin considerar que hay palabras que aparecen con mucha frecuencia.


