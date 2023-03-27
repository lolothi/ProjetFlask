import sqlite3
from flask import g,Flask

app = Flask(__name__)
PATH_DATABASE = 'imcpersonnes.db'
PATH = "/home/vincent/myproject/ProjetFlask/"

def get_db():
    return sqlite3.connect(PATH_DATABASE)	

confSQL = open(PATH+"confSQL.sql","r")

db = get_db()
#print(confSQL.read())
db.executescript(confSQL.read())




