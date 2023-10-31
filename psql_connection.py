import psycopg2
import csv

# Define la configuración de la base de datos (modificar)
db_config = {
    'dbname': 'test_connection',
    'user': 'postgres',
    'password': 'coconut',
    'host': 'localhost',
    'port': 5432
}

connection = psycopg2.connect(**db_config)
cursor = connection.cursor()

# Abre el archivo CSV
with open('C:\Users\HP\Desktop\styles\styles.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # Evitar la lectura de los nombres de la primera fila.
    next(csv_reader)
    # Crear la tabla si no existe
    cTableCommand = "CREATE TABLE IF NOT EXISTS styles (id INT, gender VARCHAR(10), masterCategory VARCHAR(25), subCategory VARCHAR(25), articleType VARCHAR(25), baseColour VARCHAR(25), season VARCHAR(10), year INT NULL, usage VARCHAR(25), productDisplayName VARCHAR(255))"
    cursor.execute(cTableCommand)

    # Iteración en cada fila
    for row in csv_reader:
        print(row)
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

# Termina la conexión con la base de datos
cursor.close()
connection.close()