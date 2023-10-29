from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

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

@app.route('/indice-invertido')
def todas_ropas():
    return render_template("indice-invertido.html")

@app.route('/PgAdmin')
def pgAdmin():
    return render_template("pgAdmin.html")
# Make sure this we are executing this file
if __name__ == '__main__':
    app.run(debug=True)
