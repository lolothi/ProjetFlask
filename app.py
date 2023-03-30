from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
NAME_DATABASE = 'imcpersonnes.db'
PATH = "./"
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

#Modify PATH to your environment
def get_db():
    return sqlite3.connect(NAME_DATABASE)	

def isAccountOK(mail,passwd) :
	db = get_db()
	reqSQL = "select passwd from Users where mail = '" + mail + "'"
	cur = db.cursor()
	req = cur.execute(reqSQL)
	res = cur.fetchone()
	if res != None :
		if res[0] == passwd :
			db.close()
			return True
		else :
			db.close()
			return False
	db.close()
	return False

def getWeightsUser(user) :
	db = get_db()
	reqSQL = "select weight from History natural join Users where Users.mail = '" + user + "' " 
	cur = db.cursor()
	req = cur.execute(reqSQL)
	res = cur.fetchall()
	if res != None :
		db.close()
		return res		
	db.close()
	return False
	
def getHeightsUser(user) :
	db = get_db()
	reqSQL = "select height from History natural join Users where Users.mail = '" + user + "' " 
	cur = db.cursor()
	req = cur.execute(reqSQL)
	res = cur.fetchall()
	if res != None :
		db.close()
		return res		
	db.close()
	return False
	
def getUserInfo(user) :
	db = get_db()
	reqSQL = "select * from Users where mail = '" + user + "' " 
	print(reqSQL)
	cur = db.cursor()
	req = cur.execute(reqSQL)
	res = cur.fetchall()
	if res != None :
		db.close()
		return res
	db.close()		
	return False
		
def setDataUser(user,weight,height) :
	db = get_db()
	reqSQL = "select id from Users where mail = '" + user + "';"
	cur = db.cursor()
	req = cur.execute(reqSQL)
	res = cur.fetchone()
	idUser = str(res[0])
	reqSQL = "insert into History (weight,height,date_create,idUser) values (" + weight + ", "+ height + ", date()," + idUser + ")"
	cur = db.cursor()
	req = cur.execute(reqSQL)
	db.commit()
	db.close()
	
def setInfoUser(username,mail,passwd,age="Null",firstName="Null",lastName="Null") :
	db = get_db()
	reqSQL = "insert into Users (username,mail,passwd,age,firstName,lastName) values ('" + username + "', '" + mail + "', '" + passwd + "', " + age + ", '" + firstName + "', '" + lastName + "')  "
	cur = db.cursor()	
	req = cur.execute(reqSQL)
	db.commit()
	db.close()

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
            user_db.append({"email": email, "passwd": passwd, "username": username})
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
    return round(poids / ((taille / 100) ** 2) , 2)

# Connect to DB
db = get_db()

# Get parameters for DB
confSQL = open("confSQL.sql", "r")

# Create tables if needed
db.executescript(confSQL.read())    
db.close()    
#Tests

setInfoUser("vincent","vincent@mail.com", "motdepasse", "25", "Vincent", "EVIEUX") #User with full infos
setInfoUser("laurent","laurent@mail.com", "motdepasselaurent") #User with partial infos 
print("Test User OK : ")
print(isAccountOK("vincent@mail.com","motdepasse"))
print(isAccountOK("laurent@mail.com","motdepasselaurent"))
print("Test insert BDD :")
setDataUser("vincent@mail.com", "70.5","177")
setDataUser("laurent@mail.com","75","180")
setDataUser("vincent@mail.com", "71.5","177")
setDataUser("laurent@mail.com","76","180")
setDataUser("vincent@mail.com", "72.5","177")
setDataUser("laurent@mail.com","77","180")
print("Test1 get infos from BDD")
print(getWeightsUser("vincent@mail.com"))
print(getHeightsUser("vincent@mail.com"))
print("Test1 get infos from BDD")
print(getWeightsUser("laurent@mail.com"))
print(getHeightsUser("laurent@mail.com"))
db = get_db()
cur = db.cursor()
print("All users")
req = cur.execute("select * from Users")
res = req.fetchall()
print(res)
db.close()
print(getUserInfo("vincent@mail.com"))
print(getUserInfo("laurent@mail.com"))
