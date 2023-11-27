from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import time
import psycopg2
import csv
import sys;
sys.path.append(r'C:\Users\ASUS\OneDrive - UNIVERSIDAD DE INGENIERIA Y TECNOLOGIA\Ciclo 5\BASE DE DATOS 2 - Sanchez Enriquez, Heider Ysaias\PROYECTOS\PROYECTO 2\proyecto_python\Project2_db2\InvertedIndex') #path to InvertedIndex
from InvertedIndex import InvertedIndex #importar la clase InvertedIndex del modulo InvertedIndex
from read_byte import get_row #importar la funcion get_row del modulo read_byte
#imrportamos la funcion init del modulo sql_Pesos
from sql_Pesos import init
#imrportamos la funcion topKpsql del modulo sql_Pesos
from sql_Pesos import topKpsql


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

indice = InvertedIndex()
@app.route('/search', methods=['POST'])
def search():
    searchTerm = request.json.get('searchTerm', None)
    print(searchTerm)
    topk = request.json.get('topk', 5)
    print(topk)

    InvertedIndexQuery = indice.processQuery(searchTerm)
    result = indice.cosine(InvertedIndexQuery,topk)

    rows = [get_row(pos_row) for pos_row in result]

    return jsonify(rows)

@app.route('/consulta', methods=['POST'])
def consulta():
    searchTerm = request.json.get('searchTerm', None)
    print(searchTerm)
    topk = request.json.get('topk', 5)
    print(topk)
    #llamar a la funcion init del modulo sql_Pesos
    #init()

    #llamar a la funcion topKpsql del modulo sql_Pesos
    rows = topKpsql(searchTerm, topk)
    # Confirma los cambios en la base de datos
    #connection.commit()
    #cursor.close()
    #connection.close()
    print("Filas que coinciden: ")
    print(rows)
    return jsonify(rows)



    





@app.route('/PgAdmin')
def pgAdmin():
    return render_template("pgAdmin.html")

@app.errorhandler(404)
def page_not_found(e):
    # nota que ahora estamos aceptando un parámetro 'e' en la función
    return "Página no encontrada", 404

# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
