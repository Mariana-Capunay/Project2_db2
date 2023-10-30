from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import time
import psycopg2
import psql_connection as psql


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
    #llamar a la funcion de consulta
    start_time = time.time()
    psql.consulta()
    end_time = time.time()
    tiempo_ejecucion = end_time - start_time
    #Definiendo la variable tableHeaders
    tableAHeaders = ["id", "gender", "masterCategory", "subCategory", "articleType", "baseColour", "season", "year", "usage", "productDisplayName"]


    #return render_template("resultados.html", resultados=resultados, tiempo_ejecucion=tiempo_ejecucion)
    return render_template("home.html", tableAHeaders=tableAHeaders, tiempo_ejecucion=tiempo_ejecucion)

    # if action == 'Indice':
    #     return jsonify({"message": "Se ha creado el índice exitosamente"})

    # elif action == 'PgAdmin':
    #     #llamar a la funcion de consulta
    #     start_time = time.time()
    #     psql.consulta()
    #     end_time = time.time()
    #     tiempo_ejecucion = end_time - start_time
    #     #mostrar los resultados
    #     #return render_template("resultados.html", resultados=resultados, tiempo_ejecucion=tiempo_ejecucion)
    #     return jsonify({"message": "Se ha creado el índice exitosamente", "tiempo_ejecucion": tiempo_ejecucion})

@app.route('/PgAdmin')
def pgAdmin():
    return render_template("pgAdmin.html")

@app.errorhandler(404)
def page_not_found():
    return jsonify({"message": "Página no encontrada, :( )"}), 404

# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
