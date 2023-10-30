from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import time
import psycopg2
import psql_connection as psql
import csv

app = Flask(__name__)

# Creating simple Routes 
@app.route('/test')
def test():
    return "Home Page"

@app.route('/test/about/')
def about_test():
    return "About Page"

# Routes to Render Something
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about', strict_slashes=False)
def about():
    return render_template("about.html")

@app.route('/consulta', methods=['POST'])
def resultados():
    query = request.form.get('query')
    topk = request.form.get('topk')
    # Define la configuración de la base de datos (modificar)
    db_config = {
    'dbname': 'test_connection',
    'user': 'postgres',
    'password': '76591212',
    'host': 'localhost',
    'port': 5432
    }
    # Realiza la consulta SQL en tu base de datos
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM styles WHERE productDisplayName ILIKE %s LIMIT %s", ('%' + query + '%', topk))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    # También obtén el tiempo de ejecución 
    return render_template("resultados.html", results=results, query=query, topk=topk)


    

@app.route('/PgAdmin')
def pgAdmin():
    return render_template("pgAdmin.html")

@app.errorhandler(404)
def page_not_found():
    return jsonify({"message": "Página no encontrada, :( )"}), 404

# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
