import json
import sqlite3
import pandas as pd


"""
Con esto leemos el fichero, obtenemos un diccionario con todo el JSON cargado y accedemos a cada uno -> [1] o [n]...
def main():
    with open("../Logs/users.json", "r") as f:
        data = json.load(f)
    print(data['usuarios'][1])
"""


"""
Recorrerse el diccionario de usuario en usuario ("Hay 30 usuarios") 1º -> Sergio Garcia 30º -> Fran Moreno
def print_json(json):
    for i in range(1, 30):
        print(i)
        print(json['usuarios'][i])
"""

"""
Crear la tabla usuarios en sqlite
c.execute("CREATE TABLE usuarios (id varchar(3), data json)")
"""

"""
Código completo para meter la data en la base de datos mis reyes <3
def main():
    with open("../Logs/users.json", "r") as f:
        data = json.load(f)
        c, conn = connect_db("../database/database.db")
        c.execute("CREATE TABLE users (id varchar(3), data json)")
        conn.commit()
        for i in range(1, 30):
            c.execute("INSERT INTO users values (?, ?)", [i, json.dumps(data['usuarios'][i])])
        conn.commit()
        conn.close()
"""


def print_json(jotason):
    for i in range(1, 30):
        print(i)
        print(jotason['usuarios'][i])


def connect_db(file):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    return c, conn


def main():
    with open("../Logs/users.json", "r") as f:
        data = json.load(f)
        c, conn = connect_db("../database/database.db")
        c.execute("CREATE TABLE users (id varchar(3), data json)")
        conn.commit()
        for i in range(1, 30):
            c.execute("INSERT INTO users values (?, ?)", [i, json.dumps(data['usuarios'][i])])
        conn.commit()
        conn.close()


if __name__ == '__main__':
    main()
