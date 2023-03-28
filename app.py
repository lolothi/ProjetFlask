import sqlite3
from flask import g,Flask

app = Flask(__name__)
NAME_DATABASE = 'imcpersonnes.db'

#Modify PATH to your environment
PATH = "/home/vincent/myproject/ProjetFlask/"

def get_db():
    return sqlite3.connect(NAME_DATABASE)	


#print(confSQL.read())


def isAccountOK(mail,passwd) :
	reqSQL = "select passwd from Users where mail = "
	reqSQL += "'" + mail + "'"
	
	cur = db.cursor()
	req = cur.execute(reqSQL)
	res = req.fetchone()
	
	if res != None :
		if res[0] == passwd :
			return True
		else :
			return False
	return False

def getWeightUser(user) :
	reqSQL = "select max(History.id), weight from History "
	reqSQL += "natural join Users "
	reqSQL += "where mail = '" + user + "' " 
	reqSQL += "group by weight "

	cur = db.cursor()
	req = cur.execute(reqSQL)
	res = req.fetchone()
	
	if res != None :
		return res[1]		
	return False
	
def getHeightUser(user) :
	reqSQL = "select max(History.id), height from History "
	reqSQL += "natural join Users "
	reqSQL += "where mail = '" + user + "' " 
	reqSQL += "group by height "

	cur = db.cursor()
	req = cur.execute(reqSQL)
	res = req.fetchone()
	
	if res != None :
		return res[1]		
	return False
	
def getUserInfo(user) :
	reqSQL = "select firstName, lastName,age from Users "
	reqSQL += "where mail = '" + user + "' " 
	
	cur = db.cursor()
	req = cur.execute(reqSQL)
	res = req.fetchone()
	
	if res != None :
		return res
	return False
		
#Get parameters for DB
confSQL = open(PATH+"confSQL.sql","r")

#Connect to DB
db = get_db()

#Create tables if needed
db.executescript(confSQL.read())

#Tests
#db.execute("insert into Users (lastName,firstName,mail,passwd,age) values ('EVIEUX','Vincent','vincent@mail.com','motdepasse',25)")
#db.execute("insert into History (height,weight,idUser,date_create) values (177,70.5,1,'2022-03-28')")
#print(isAccountOK("vincent@mail.com","motdepasse"))
#print(getWeightUser("vincent@mail.com"))
#print(getHeightUser("vincent@mail.com"))
#print(getUserInfo("vincent@mail.com"))








