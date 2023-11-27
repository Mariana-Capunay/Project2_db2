import psycopg2
import csv

ruta_csv = 'C:/Users/ASUS/Downloads/prueba/styles.csv'
#ruta_csv = 'C:/Users/HP/Desktop/styles/styles.csv'
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
    with open(ruta_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # Evitar la lectura de los nombres de la primera fila.
        next(csv_reader)
        # Crear la tabla si no existe
        cTableCommand = "CREATE TABLE IF NOT EXISTS styles (id INT, gender VARCHAR(10), masterCategory VARCHAR(25), subCategory VARCHAR(25), articleType VARCHAR(25), baseColour VARCHAR(25), season VARCHAR(10), year INT NULL, usage VARCHAR(25), productDisplayName VARCHAR(255))"
        cursor.execute(cTableCommand)

        # Iteración en cada fila
        for row in csv_reader:
            print(row,'mari')
            # Caso especial si se registran más de 10 elementos en una fila
            while len(row) > 10:
                print("Sz: ", len(row))
                print("Caso especial: ", row[len(row)-1])
                row[len(row)-2] += row[len(row)-1]
                row.pop()
                print("Nuevo display name: ", row[len(row)-2])
                print("Sz: ", len(row))
            id, gender, masterCategory, subCategory, articleType, baseColour, season, stryear, usage, productDisplayName = row
            if stryear == '':
                year = None
            else:
                year = int(stryear)

            # Inserta la fila en la base de datos
            cursor.execute("INSERT INTO styles (id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, gender, masterCategory, subCategory, articleType, baseColour, season, year, usage, productDisplayName))
        # Confirma los cambios en la base de datos
        connection.commit()
    cursor.execute("ALTER TABLE styles ADD COLUMN weighted_tsv tsvector")
    cursor.execute("ALTER TABLE styles ADD COLUMN weighted_tsv2 tsvector")
    cursor.execute("UPDATE styles SET weighted_tsv = x.weighted_tsv, weighted_tsv2 = x.weighted_tsv FROM (SELECT id, setweight(to_tsvector('english', COALESCE(masterCategory,'')), 'A') || setweight(to_tsvector('english', COALESCE(articleType,'')), 'A') || setweight(to_tsvector('english', COALESCE(baseColour,'')), 'A') || setweight(to_tsvector('english', COALESCE(season,'')), 'A') || setweight(to_tsvector('english', COALESCE(usage,'')), 'A') || setweight(to_tsvector('english', COALESCE(productdisplayname,'')), 'B') AS weighted_tsv FROM styles) AS x WHERE x.id = styles.id;")
    cursor.execute("CREATE INDEX weighted_tsv_idx ON styles USING GIN (weighted_tsv2)")
    connection.commit()
    cursor.close()

def topKpsql(query, k):
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    words = query.split(" ")
    terms = ""
    for word in words:
        terms += word + " & "
    terms = terms[:-2]
    
    print("Terminos leidos: ", terms)

    cursor.execute("set enable_seqscan = false")

    # first idea
    #consulta = f"SELECT id, gender, mastercategory, subcategory, articletype, basecolour, season, year, usage, productdisplayname FROM styles, to_tsquery('english', '{terms}') query WHERE query @@ weighted_tsv2 ORDER BY ts_rank_cd(weighted_tsv2, query) desc LIMIT {k};"

    consulta = f"""SELECT id, gender, mastercategory, subcategory, articletype, basecolour, season, year, usage, productdisplayname 
                FROM(
                    SELECT 
                    id, 
                    gender, 
                    mastercategory, 
                    subcategory, 
                    articletype, 
                    basecolour, 
                    season, 
                    year, 
                    usage, 
                    productdisplayname,
                    ts_rank_cd(weighted_tsv2, to_tsquery('english', '{terms}')) AS similarity
                    FROM styles 
                    WHERE to_tsquery('english','{terms}') @@ weighted_tsv2 
                    ORDER BY similarity DESC LIMIT {k}
                ) AS R"""
    
    cursor.execute(consulta)
    rows = cursor.fetchall()
    
    
    if len(rows)<k: # if we have less rows than k, we search with "|"
        terms = ""
        for word in words:
            terms += word + " | "
        terms = terms[:-2]
        consulta = f"""SELECT id, gender, mastercategory, subcategory, articletype, basecolour, season, year, usage, productdisplayname 
                FROM(
                    SELECT 
                    id, 
                    gender, 
                    mastercategory, 
                    subcategory, 
                    articletype, 
                    basecolour, 
                    season, 
                    year, 
                    usage, 
                    productdisplayname,
                    ts_rank_cd(weighted_tsv2, to_tsquery('english', '{terms}')) AS similarity
                    FROM styles 
                    WHERE to_tsquery('english', '{terms}') @@ weighted_tsv2 
                    ORDER BY similarity DESC 
                    LIMIT {k-len(rows)}
                ) AS R""" # we search the top (k-rows we have)
        cursor.execute(consulta)

        rows2 = cursor.fetchall()# now, we append the new rows in the list
        for new_row in rows2:
            rows.append(new_row)
    for row in rows:
        print(row)
    return rows

#init()
query = "yellow casual pants are yellow"
k = 5

topKpsql(query, k)

# Termina la conexión con la base de datos
cursor.close()
connection.close()