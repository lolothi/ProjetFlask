

CREATE TABLE IF NOT EXISTS Users (
id integer primary key autoincrement, 
lastName VARCHAR(30), 
firstName VARCHAR(30), 
mail VARCHAR(30)NOT NULL UNIQUE, 
passwd VARCHAR(30)NOT NULL, 
age integer
);


CREATE TABLE IF NOT EXISTS History (id integer primary key autoincrement, 
height double, 
weight double, 
idUsers integer, 
date_create date,
FOREIGN KEY (idUsers) REFERENCES Users(id)
);


