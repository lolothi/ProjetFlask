from flask import Flask, render_template, request, session, redirect, url_for
from enum import Enum
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

NAME_DATABASE = "imcpersonnes.db"


def get_db():
    return sqlite3.connect(NAME_DATABASE, check_same_thread=False)


def isAccountOK(mail, passwd):
    db = get_db()
    reqSQL = f"select username from Users where mail = '{mail}' AND passwd = '{passwd}'"
    cur = db.cursor()
    cur.execute(reqSQL)
    response = cur.fetchone()
    db.close()
    if response:
        return True

def getIMCInfoUser(user):
	db = get_db()
	reqSQL = f"select height,weight,date_create from History join Users on (History.idUser = Users.id) where Users.mail = '{user}' "
	cur = db.cursor()
	cur.execute(reqSQL)
	res = cur.fetchall()
	if res:
		db.close()
		return res
	db.close()


def getUserInfo(user):
	db = get_db()
	reqSQL = f"select * from Users where mail = '{user}' "
	print(reqSQL)
	cur = db.cursor()
	cur.execute(reqSQL)
	res = cur.fetchone()
	if res:
		db.close()
		return res
	db.close()
	return False


def setDataUser(user, weight, height):
    db = get_db()
    reqSQL = f"select id from Users where mail = '{user}';"
    cur = db.cursor()
    cur.execute(reqSQL)
    res = cur.fetchone()
    idUser = str(res[0])
    reqSQL = f"insert into History (weight,height,date_create,idUser) values ({weight}, {height}, date(),{idUser})"
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


def setInfoUser(username, mail, passwd, age="", firstName="", lastName=""):
    db = get_db()
    reqSQL = f"insert into Users (username,mail,passwd,age,firstName,lastName) values ('{username}', '{mail}', '{passwd}', '{age}', '{firstName}', '{lastName}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


def updateInfoUser(userID, username, mail, passwd, age, firstName, lastName):
    db = get_db()
    reqSQL = f"update Users set lastName = '{lastName}',firstName = '{firstName}',username = '{username}', mail = '{mail}', passwd = '{passwd}', age = '{age}' where id = {userID}"
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()

@app.route("/")
def main_page():
    if session.get('user'):
        return render_template("home.html",history=imcHistory()[0],imcList=imcHistory()[1])
    return render_template("home.html")


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
        if isAccountOK(email, passwd):
            username = getUserInfo(email)[USER_PARAMS.USERNAME.value]
            session["user"] = {"email": email, "username": username}
            message = "utilisateur connecté"
            return redirect("/")
        else:
            error = "mauvais utilisateur/mot de passe"

    return render_template("login.html", message=message, error=error, connected_user=connected_user)


# Register user if new one
@app.route("/register", methods=["POST", "GET"])
def register():
    message = None
    error = None
    email = request.form.get("email")
    passwd = request.form.get("passwd")
    username = request.form.get("username")

    if request.method == "POST":
        if email and passwd:
            try:
                setInfoUser(username, email, passwd)
                session["user"] = {"email": email, "username": username}
                message = "utilisateur créé"
                return redirect("/")
            except:
                error = "Erreur dans la création de l'utilisateur"

    return render_template("register.html", error=error, message=message)


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

    lastName = currentUser[USER_PARAMS.LAST_NAME.value]
    firstName = currentUser[USER_PARAMS.FIRST_NAME.value]
    username = currentUser[USER_PARAMS.USERNAME.value]
    password = currentUser[USER_PARAMS.PASSWORD.value]
    email = currentUser[USER_PARAMS.EMAIL.value]
    age = currentUser[USER_PARAMS.AGE.value]

    if request.method == "POST":

        dom_lastName = request.form.get("lastName")
        dom_firstName = request.form.get("firstName")
        dom_username = request.form.get("username")
        dom_password = request.form.get("password")
        dom_email = request.form.get("email")
        dom_age = request.form.get("age")

        if len(dom_username) > 0 and len(dom_email) > 0 and len(dom_password) > 0 :
            updateInfoUser(currentUser[0], dom_username, dom_email,
                           dom_password, dom_age, dom_firstName, dom_lastName)
            session["user"] = {"email": dom_email, "username": dom_username}

            return redirect("/")
        else:
            error = "One of the required fields is null"

    return render_template("user-profil.html", lastName=lastName, firstName=firstName, 
                           username=username, email=email, password=password, age=age, error=error)

# Connect to DB
db = get_db()

# Get parameters for DB
confSQL = open("confSQL.sql", "r")

# Create tables if needed
db.executescript(confSQL.read())
db.close()


@app.route("/imc", methods=["POST", "GET"])
def imc():  # computes imc and returns it so it can be shown to users
    if request.method == "POST":  # when posting, we compute imc, save it to base then show it to the user
        imc = compute_imc(float(request.form["poids"]),float(request.form["taille"]))
        # colours front
        imc_color = "rouge" if imc < 16 or imc >= 26 else "jaune" if imc < 18 else "vert"
        if session.get('user'):
            setDataUser(session["user"]["email"], float(
                request.form["poids"]), float(request.form["taille"]))
            # rendering with result and with user
            return render_template('imc.html', imc=imc, imc_color=imc_color,history=imcHistory()[0],imcList=imcHistory()[1])
        # rendering with result and without user
        return render_template('imc.html', imc=imc, imc_color=imc_color)
    if session.get('user'):
        return render_template("imc.html",history=imcHistory()[0],imcList=imcHistory()[1])  # when GET, render empty form
    return render_template("imc.html")

def compute_imc(weight,height):
    return round(weight / ((height / 100.0) ** 2), 2)

def imcHistory():
    imcList = list()
    history = getIMCInfoUser(session["user"]["email"])
    if history:
        for line in history:
            imcList.append(compute_imc(line[1],line[0]))
    return (history,imcList)

USER_PARAMS = Enum('User',['ID','LAST_NAME','FIRST_NAME','USERNAME','EMAIL','PASSWORD','AGE'], start=0)