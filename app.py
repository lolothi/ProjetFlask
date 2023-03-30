from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)

NAME_DATABASE = "imcpersonnes.db"
# Modify PATH to your environment
PATH = "./"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def get_db():
    return sqlite3.connect(NAME_DATABASE, check_same_thread=False)


def isAccountOK(mail, passwd):
    reqSQL = "select passwd from Users where mail = "
    reqSQL += "'" + mail + "'"
    
    cur = db.cursor()
    req = cur.execute(reqSQL)
    res = req.fetchone()

    if res != None:
        if res[0] == passwd:
            return True
        else:
            return False
    return False


def getWeightUser(user):
    reqSQL = "select max(History.id), weight from History "
    reqSQL += "natural join Users "
    reqSQL += "where mail = '" + user + "' "
    reqSQL += "group by weight "

    cur = db.cursor()
    req = cur.execute(reqSQL)
    res = req.fetchone()

    if res != None:
        return res[1]
    return False


def getHeightUser(user):
    reqSQL = "select max(History.id), height from History "
    reqSQL += "natural join Users "
    reqSQL += "where mail = '" + user + "' "
    reqSQL += "group by height "
    cur = db.cursor()
    req = cur.execute(reqSQL)
    res = req.fetchone()

    if res != None:
        return res[1]
    return False


def getUserInfo(user):
    reqSQL = "select * from Users "
    reqSQL += "where mail = '" + user + "' "

    cur = db.cursor()
    req = cur.execute(reqSQL)
    res = req.fetchone()

    if res != None:
        return res
    return False


# welcome page
@app.route("/")
def main_page():
    return render_template("index.html")


# Login
user_db = []  # Liste de dict : en attendant l'acces à la db


@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    message = None
    email = request.form.get("email")
    passwd = request.form.get("passwd")

    try:
        # check if user is connected
        connected_user = session["user"]["username"]
    except:
        session["user"] = None
        connected_user = None
    if request.method == "POST":
        # vérifier l'existence de l'email dans la db (list of dict)
        # if (any(email in d['email'] for d in user_db)):
        for user in user_db:
            if email == user["email"]:
                if passwd == user["passwd"]:
                    session["user"] = {"email": email, "username": user["username"]}
                    connected_user = user["username"]
                    message = "utilisateur connecté"
                    return redirect("/imc")
                else:
                    message = None
                    error = "mauvais mot de passe"
                    break
        else:
            error = "mauvais utilisateur/mot de passe"

    return render_template("login.html", message=message, error=error, connected_user=connected_user)


# Register user if new one
@app.route("/register", methods=["POST", "GET"])
def register():
    message = None
    email = request.form.get("email")
    passwd = request.form.get("passwd")
    username = request.form.get("username")

    if request.method == "POST":
        if email and passwd:
            db.execute(f"insert into Users (lastName,firstName,username,mail,passwd,age) values ('','','{username}','{email}','{passwd}','')")
            session["user"] = {"email": email, "username": username}
            message = "utilisateur créé"

    return render_template("register.html", message=message)


# Logout user if connected
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# User profile
@app.route("/user", methods=["GET", "POST"])
def profil():
    error = None
    currentUser = getUserInfo(session["user"]["email"])
    username = currentUser[2]
    password = currentUser[4]
    email = currentUser[5]
    age = currentUser[6]

    if request.method == "POST":

        dom_username = request.form.get("username")
        dom_password = request.form.get("password")
        dom_email = request.form.get("email")
        dom_age = request.form.get("age")

        if valid_profil(dom_username, dom_password, dom_email, dom_age):
            db.execute(f"update Users set lastName = '',firstName = '',username = '{dom_username}', mail = '{dom_email}', passwd = '{dom_password}', age = '{dom_age}' where id = {currentUser[0]}")
            session["user"] = {"email": dom_email, "username": dom_username}

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

#######################################################################
# Connect to DB
db = get_db()

# Get parameters for DB
confSQL = open("confSQL.sql", "r")

# Create tables if needed
db.executescript(confSQL.read())

#Sample pour IMC
# db.execute("insert into History (height,weight,idUser,date_create) values (177,70.5,1,'2022-03-28')")