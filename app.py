from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

html = "index.html"
# session['user'] = 'None'


# Page d'accueil
@app.route("/")
def main_page():
    return render_template('index.html')

user_db = []
# Login
@app.route('/login', methods=['POST', 'GET'])
def login(): 

    try:
        connected_user = session['user']
    except:
        session['user'] = None
        connected_user = None

    print('--DB--',user_db)
    connected_user = None
    error = None
    email = request.form.get('email')
    password = request.form.get('password')

    # if session['user']:
    #     connected_user = session['user']

    if request.method == 'POST':
        for user in user_db:
            if email == user['email']:
                print('--LOGIN--DEDANS')
                session['user']= email
                

        # return render_template('index.html')
    #     if valid_login(request.form['username'],
    #                    request.form['password']):
    #         return log_the_user_in(request.form['username'])
    #     else:
    #         error = 'Invalid username/password'
    return render_template('login.html', error=error, connected_user=connected_user)

@app.route('/register', methods=['POST', 'GET'])
def register(): 
    error = None
    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == 'POST':
        if email and password:
            user_db.append({"email":email, "password":password})
            print('--register--',user_db)

        # return render_template('index.html')
    #     if valid_login(request.form['username'],
    #                    request.form['password']):
    #         return log_the_user_in(request.form['username'])
    #     else:
    #         error = 'Invalid username/password'
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    session.pop('user', None)
    # session['user'] = None
    # return redirect(url_for('index.html'))
    return render_template('logout.html')

# IMC
@app.route("/imc")
def imc():
    return render_template('index.html')


# User profile
@app.route("/user")
def profil():
    return render_template('index.html')
