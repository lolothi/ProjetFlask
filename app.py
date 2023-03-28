from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import sqlite3


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

PATH_DATABASE = "imcpersonnes.db"
PATH = "./"


def get_db():
    return sqlite3.connect(PATH_DATABASE)


confSQL = open(PATH + "confSQL.sql", "r")

db = get_db()
# print(confSQL.read())
db.executescript(confSQL.read())

# html = "index.html"

# Page d'accueil
@app.route("/")
def main_page():
    return render_template("index.html")


# Login
user_db = []  #en attendant l'acces à la db
@app.route("/login", methods=["POST", "GET"])
def login():

    try:
        connected_user = session["user"]
    except:
        session["user"] = None
        print("SESSION DECONNECTIOn")
        connected_user = None

    print("--DB--", user_db)
    error = None
    message = None
    email = request.form.get("email")
    password = request.form.get("password")

    if request.method == "POST":
        # vérifier l'existence de l'email dans la db (list of dict)
        # if (any(email in d['email'] for d in user_db)):
        for user in user_db:
            if email == user["email"]:
                if password == user["password"]:
                    session["user"] = email
                    connected_user = email
                    message = "utilisateur connecté"
                    break
                else:
                    message = None
                    error = "mauvais mot de passe"
                    break
        else:
            error = "mauvais utilisateur/mot de passe"

    return render_template("login.html", message=message, error=error, connected_user=connected_user)


@app.route("/register", methods=["POST", "GET"])
def register():
    message = None
    email = request.form.get("email")
    password = request.form.get("password")

    if request.method == "POST":
        if email and password:
            user_db.append({"email": email, "password": password})
            message = "utilisateur créé"

    return render_template("register.html", message=message)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect('/')


# User profile
@app.route("/user", methods=["GET", "POST"])
def profil():
    error = None

    # TODO : Get from DB
    username = ""
    password = ""
    email = ""
    age = None

    if request.method == "POST":

        dom_username = request.form.get("username")
        dom_password = request.form.get("password")
        dom_email = request.form.get("email")
        dom_age = request.form.get("age")

        if valid_profil(dom_username, dom_password, dom_email, dom_age):
            session["user"] = dom_email
            # TODO : Update user row in db
            return redirect("/imc")
        else:
            error = "One of the fields is null"

    return render_template("user-profil.html", username=username, email=password, password=email, age=age, error=error)


def valid_profil(username: str, email: str, password: str, age: str):
    if len(username) == 0 or len(email) == 0 or len(password) == 0 or len(age) == 0:
        return False
    return True


@app.route("/imc", methods=["POST", "GET"])
def imc():
    if request.method == "POST":
        poids = float(request.form["poids"])
        taille = float(request.form["taille"])
        imc = computeImc(poids, taille)
        if imc:
            if imc < 16:
                imc_color = "rouge"
            elif imc < 18:
                imc_color = "jaune"
            elif imc < 24:
                imc_color = "vert"
            elif imc < 26:
                imc_color = "jaune"
            else:
                imc_color = "rouge"

        # redirect vers /imc
        return render_template(
            "imc.html", imc=imc, imc_color=imc_color
        )  # passe le résultat de l'IMC à votre modèle HTML

    return render_template("imc.html")


def computeImc(poids, taille):
    return round(poids / ((taille / 100) ** 2), 2)
