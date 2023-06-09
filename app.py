from flask import Flask, render_template, request, session, redirect
from enum import Enum
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

NAME_DATABASE = "BMIDatabase.db"


def get_db():
    """Connect the sqlite Database"""
    return sqlite3.connect(NAME_DATABASE, check_same_thread=False)


def isAccountOK(mail, passwd):
    """Check if the using exists in the DB"""
    db = get_db()
    reqSQL = f"select username from Users where mail = '{mail}' AND passwd = '{passwd}'"
    cur = db.cursor()
    cur.execute(reqSQL)
    response = cur.fetchone()
    db.close()
    if response:
        return True


def getBMIInfoUser(user):
    """Read the BMI's history of the connected user"""
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
    """Read the information of the connected user"""
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
    """Read the BMI's history of the connected user"""
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
    """Create the information of the connected user"""
    db = get_db()
    reqSQL = f"insert into Users (username,mail,passwd,age,firstName,lastName) values ('{username}', '{mail}', '{passwd}', '{age}', '{firstName}', '{lastName}')  "
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


def updateInfoUser(userID, username, mail, passwd, age, firstName, lastName):
    """Update the information of the connected user"""
    db = get_db()
    reqSQL = f"update Users set lastName = '{lastName}',firstName = '{firstName}',username = '{username}', mail = '{mail}', passwd = '{passwd}', age = '{age}' where id = {userID}"
    cur = db.cursor()
    cur.execute(reqSQL)
    db.commit()
    db.close()


@app.route("/")
def main_page():
    """Display the welcome page
    @If connected user, display the connected user's history of BMI"""
    if session.get("user"):
        return render_template("home.html", history=BMIHistory()[0], BMIList=BMIHistory()[1])
    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    """Connect existant user"""
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
            message = "User connected"
            return redirect("/")
        else:
            error = "Wrong user/password"

    return render_template("login.html", message=message, error=error, connected_user=connected_user)


@app.route("/register", methods=["POST", "GET"])
def register():
    """Create new user in the database"""
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
                message = "User created"
                return redirect("/")
            except:
                error = "Error in user creation"

    return render_template("register.html", error=error, message=message)


@app.route("/logout")
def logout():
    """Disconnect the connected user"""
    session.pop("user", None)
    return redirect("/")


@app.route("/user", methods=["GET", "POST"])
def profil():
    """Display the user's account, possibility to update the information"""
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

        if len(dom_username) > 0 and len(dom_email) > 0 and len(dom_password) > 0:
            updateInfoUser(currentUser[0], dom_username, dom_email, dom_password, dom_age, dom_firstName, dom_lastName)
            session["user"] = {"email": dom_email, "username": dom_username}

            return redirect("/")
        else:
            error = "One of the required fields is null"

    return render_template(
        "user-profil.html",
        lastName=lastName,
        firstName=firstName,
        username=username,
        email=email,
        password=password,
        age=age,
        error=error,
    )


# Connect to DB
db = get_db()

# Get parameters for DB
confSQL = open("confSQL.sql", "r")

# Create tables if needed
db.executescript(confSQL.read())
db.close()


@app.route("/BMI", methods=["POST", "GET"])
def BMI():
    """Compute BMI and return it so it can be shown to users"""
    if request.method == "POST":  # when posting, we compute BMI, save it to base then show it to the user
        BMI = compute_BMI(float(request.form["weight"]), float(request.form["height"]))
        # colors front
        BMI_color = "red" if BMI < 16 or BMI >= 26 else "yellow" if BMI < 18 else "green"
        if session.get("user"):
            setDataUser(session["user"]["email"], float(request.form["weight"]), float(request.form["height"]))
            # rendering with result and with user
            return render_template(
                "bmi.html", BMI=BMI, BMI_color=BMI_color, history=BMIHistory()[0], BMIList=BMIHistory()[1]
            )
        # rendering with result and without user
        return render_template("bmi.html", BMI=BMI, BMI_color=BMI_color)
    if session.get("user"):
        return render_template(
            "bmi.html", history=BMIHistory()[0], BMIList=BMIHistory()[1]
        )  # when GET, render empty form
    return render_template("bmi.html")


def compute_BMI(weight, height):
    """Caculates the BMI from weight and height"""
    return round(weight / ((height / 100.0) ** 2), 2)


def BMIHistory():
    """Read connected user's history BMI event from database"""
    BMIList = list()
    history = getBMIInfoUser(session["user"]["email"])
    if history:
        for line in history:
            BMIList.append(compute_BMI(line[1], line[0]))
    return (history, BMIList)


USER_PARAMS = Enum("User", ["ID", "LAST_NAME", "FIRST_NAME", "USERNAME", "EMAIL", "PASSWORD", "AGE"], start=0)
