import psycopg2

# Define la configuración de tu base de datos
db_config = {    
    'dbname': 'test_connection',
    'user': 'postgres',
    'password': '76591212',
    'host': 'localhost',
    'port': 5432
}

try:
    # Establece la conexión
    connection = psycopg2.connect(**db_config)
    print("¡Conexión exitosa!")

    # Crea un cursor para ejecutar consultas
    cursor = connection.cursor()

    # Ejemplo de consulta
    cursor.execute("SELECT * FROM tu_tabla;")
    rows = cursor.fetchall()

    # Muestra los resultados
    for row in rows:
        print(row)

    # Cierra el cursor y la conexión
    cursor.close()
    connection.close()

except psycopg2.Error as error:
    print("Error al conectar a la base de datos:", error)
