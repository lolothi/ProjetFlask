from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

html = "index.html"

# Page d'accueil
@app.route("/")
def main_page():
    return render_template('index.html')

# Login
@app.route("/login")
def login():
    return render_template('index.html')

# IMC
@app.route("/imc")
def imc():
    return render_template('index.html')

# User profile
@app.route("/user", methods=['GET', 'POST'])
def profil():
    error = None

    #TODO : Get from DB
    username = ""
    password = ""
    email = ""
    age = None

    if request.method == 'POST':

        dom_username = request.form.get('username')
        dom_password = request.form.get('password')
        dom_email = request.form.get('email')
        dom_age = request.form.get('age')

        if(valid_profil(dom_username,dom_password,dom_email,dom_age)):
            session['user'] = dom_email
            #TODO : Update user row in db
            return redirect("/imc")
        else:
            error = "One of the field is null"
    
    return render_template(
        'user-profil.html', 
        username = username, 
        email = password, 
        password = email,
        age = age,
        error = error)

def valid_profil(username:str,email:str,password:str,age:str):
    if(len(username) == 0 or len(email) == 0 or len(password) == 0 or len(age) == 0):
        return False
    return True