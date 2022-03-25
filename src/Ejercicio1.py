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
Solo mete el string en JSON, voy a intentar meter dato a dato en la tabla para olvidarnos de json luego
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


def leer_datos():
    # Abrir los ficheros
    datos_legal = open("../Logs/legal.json", "r")
    datos_users = open("../Logs/users.json", "r")
    # Nos cargamos el diccionarios el contenido en jotason
    legal = json.load(datos_legal)
    users = json.load(datos_users)
    # Cerramos los ficheros para ser gente de bien
    datos_legal.close()
    datos_users.close()
    # Retornamos valores
    return legal, users


# https://stackoverflow.com/questions/18552001/accessing-dict-keys-element-by-index-in-python3
# Para sacar los valores de cada key he usado esto, bastante fino
def insertar_datos(legal, users):
    c, conn = connect_db("../database/database.db")
    create_tables(c, conn)
    for i in legal['legal']:
        for j in i.keys():
            print(i)  # {'www.nbcckcip.com': {'cookies': 0, 'aviso': 1, 'proteccion_de_datos': 0, 'creacion': 2002}}
            print(i[j])  # Esto imprime ->{'cookies': 0, 'aviso': 1, 'proteccion_de_datos': 0, 'creacion': 2002}
            print(i[j]["cookies"])  # Esto imprime -> 0
            print(i[j]["creacion"]) # Esto imprime -> 2007

def connect_db(file):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    return c, conn


def create_tables(c, conn):
    # Borrar tablas antes de volver a crear
    c.execute("DROP TABLE IF EXISTS users")
    c.execute("DROP TABLE IF EXISTS legal")
    # Crear las tablas para los datos
    # En emails, no se me ha ocurrido otra cosa que separar en 3 el apartado de emails (siempre son 3 datos)
    # TODO no he hecho la parte de fechas, creo que tendría que ir en una tabla aparte con clave foránea a users
    # TODO lo mismo que el anterior comentario pero con las IPs, está en array de n valores arbitrarios
    c.execute(("CREATE TABLE legal"
               "(url data , cookies integer, aviso integer, "
               "proteccion_datos integer, creacion integer, "
               "PRIMARY KEY(url))"))
    c.execute("CREATE TABLE users (username text, telefono integer , contrasena text, provincia text, "
              "permisos bool, emails_total integer , emails_phishing integer , emails_ciclados integer, "
              "PRIMARY KEY(username))")

    conn.commit()
    return


def main():
    legal, users = leer_datos()
    insertar_datos(legal, users)


if __name__ == '__main__':
    main()
