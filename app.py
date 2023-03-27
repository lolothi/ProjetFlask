from flask import Flask, render_template, request, jsonify

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

@app.route("/imc", methods=['POST', 'GET'])
def imc():
    if request.method == 'POST':
        poids = float(request.form['poids'])
        taille = float(request.form['taille'])
        imc = computeImc(poids, taille)
        if imc:
            if imc < 16:
                imc_color = "rouge"
            elif imc < 18:
                imc_color = "jaune"
            elif imc < 24:
                imc_color = "vert"
            elif imc <26:
                imc_color="jaune"
            else:
                imc_color = "rouge"
    
        #redirect vers /imc
        return render_template('imc.html', imc=imc, imc_color=imc_color) # passe le résultat de l'IMC à votre modèle HTML
    
    return render_template('imc.html')


def computeImc(poids, taille):
    return round(poids / ((taille / 100) ** 2) , 2)
