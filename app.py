from flask import Flask, render_template

app = Flask(__name__)

html = "index.html"


# Page d'accueil
@app.route("/")
def main_page():
    return render_template('index.html')


# Login
@app.route("/login")
def login():
    return render_template('index.html')

# User profile
@app.route("/user")
def profil():
    return render_template('index.html')

#IMC
@app.route("/imc")
def imc():
    return render_template('imc.html')

