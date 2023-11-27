import psycopg2
import csv

# Define la configuración de la base de datos (modificar)
db_config = {
    'dbname': 'test_connection',
    'user': 'postgres',
    'password': '76591212',
    'host': 'localhost',
    'port': 5432
}

connection = psycopg2.connect(**db_config)
cursor = connection.cursor()

def init():
# Abre el archivo CSV
    #with open('C:/Users/HP/Desktop/styles/styles.csv', 'r') as csv_file:
    with open('C:/Users/ASUS/Downloads/prueba/styles.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # Evitar la lectura de los nombres de la primera fila.
        next(csv_reader)
        # Crear la tabla si no existe
        cTableCommand = "CREATE TABLE IF NOT EXISTS styles (id INT, gender VARCHAR(10), masterCategory VARCHAR(25), subCategory VARCHAR(25), articleType VARCHAR(25), baseColour VARCHAR(25), season VARCHAR(10), year INT NULL, usage VARCHAR(25), productDisplayName VARCHAR(255))"
        cursor.execute(cTableCommand)
        
        # Iteración en cada fila
        for row in csv_reader:
            #print(row)
            # Caso especial si se registran más de 10 elementos en una fila
            while len(row) > 10:
                #print("Sz: ", len(row))
                #print("Caso especial: ", row[len(row)-1])
                row[len(row)-2] += row[len(row)-1]
                row.pop()
                #print("Nuevo display name: ", row[len(row)-2])
                #print("Sz: ", len(row))
            id, gender, masterCategory, subCategory, articleType, baseColour, season, stryear, usage, productDisplayName = row
            if stryear == '':
                year = None
            else:
                year = int(stryear)

            # Inserta la fila en la base de datos si no está vacía
            # Verifica si hay alguna fila en la tabla
            
            cursor.execute("SELECT 1 FROM styles LIMIT 1")
            if cursor.fetchone() is None:
                # Si no hay ninguna fila en la tabla, inserta la nueva fila
                cursor.execute("INSERT INTO styles (id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName))


            # Confirma los cambios en la base de datos
        connection.commit()
    cursor.execute("ALTER TABLE styles ADD COLUMN weighted_tsv tsvector")
    cursor.execute("ALTER TABLE styles ADD COLUMN weighted_tsv2 tsvector")
    cursor.execute("UPDATE styles SET weighted_tsv = x.weighted_tsv, weighted_tsv2 = x.weighted_tsv FROM (SELECT id, setweight(to_tsvector('english', COALESCE(masterCategory,'')), 'A') || setweight(to_tsvector('english', COALESCE(articleType,'')), 'A') || setweight(to_tsvector('english', COALESCE(baseColour,'')), 'A') || setweight(to_tsvector('english', COALESCE(season,'')), 'A') || setweight(to_tsvector('english', COALESCE(usage,'')), 'A') || setweight(to_tsvector('english', COALESCE(productdisplayname,'')), 'B') AS weighted_tsv FROM styles) AS x WHERE x.id = styles.id;")
    cursor.execute("CREATE INDEX weighted_tsv_idx ON styles USING GIN (weighted_tsv2)")

def topKpsql(query, k):
    words = query.split(" ")
    terms = ""
    for word in words:
        terms += word + " | "
    terms = terms[:-2]
    
    print("Terminos leidos: ", terms)

    cursor.execute("set enable_seqscan = false")
    print("hola")
    consulta = f"SELECT id, gender, mastercategory, subcategory, articletype, basecolour, season, year, usage, productdisplayname FROM styles, to_tsquery('english', '{terms}') query WHERE query @@ weighted_tsv2 ORDER BY ts_rank_cd(weighted_tsv2, query) desc LIMIT {k};"
    print("hola")
    cursor.execute(consulta)
    print("hola")
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# Inicializa la base de datos
init()
query = "adidas shoes red"
k = 5

topKpsql(query, k)

# Termina la conexión con la base de datos
#cursor.close()
#connection.close()