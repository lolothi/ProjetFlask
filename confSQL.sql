

CREATE TABLE IF NOT EXISTS Users (
id integer primary key autoincrement, 
lastName VARCHAR(30), 
firstName VARCHAR(30), 
username VARCHAR(30) NOT NULL,
mail VARCHAR(30)NOT NULL UNIQUE, 
passwd VARCHAR(30)NOT NULL, 
age smallint
);


CREATE TABLE IF NOT EXISTS History (
id integer primary key autoincrement, 
height smallint, 
weight decimal(4,2), 
idUser integer, 
date_create date,
FOREIGN KEY (idUser) REFERENCES Users(id)
);


