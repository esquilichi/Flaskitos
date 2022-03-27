import json
import sqlite3
import pandas as pd
import base64

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
#
# Funciones auxiliares para interpretar arrays
tb64 = lambda x: base64.b64encode(str(x).encode('UTF-8')) #Conversor a base64 para almacenar en bbdd
fb64 = lambda x: list(base64.b64decode(x).decode('UTF-8').strip('[]').replace('\'', '').split(', ')) #Conversor desde base64 para dataframe
clist = lambda x: x.str.len()  #Conversor de listas a n elementos



def create_dataframes() -> pd.DataFrame:
    c, conn = connect_db("../database/database.db")
    dframe = pd.read_sql_query("SELECT * FROM users", conn)

    dframe['ips'] = dframe['ips'].apply(fb64)
    dframe['fechas'] = dframe['fechas'].apply(fb64)

    #print(dframe['fechas'])
    #print(dframe['ips'])
    #print("Maximo de fechas",clist(dframe['fechas']).max())
    print("Minimo de ips\n", clist(dframe['ips']))
    #print(tlistdf(dframe['fechas']).value_counts())
    #dframe.ips = str(fb64(dframe.ips))
    #print(dframe)

    pass

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
    lista = list()
    # Guardar todos los datos en una sola lista para hacer un insert del tirón, mucho más facil que ir 1 a 1
    for i in legal['legal']:
        for j in i.keys():
            mytuple = (j, i[j]["cookies"], i[j]["aviso"], i[j]["proteccion_de_datos"], i[j]["creacion"])
            lista.append(mytuple)
        c.executemany('INSERT OR IGNORE INTO legal VALUES(?,?,?,?,?)', lista)
    conn.commit()

    lista = list()
    for i in users['usuarios']:
        for j in i.keys():

            a = tb64(i[j]['fechas'])
            l = fb64(a)
            #print(l)
            mytuple = (j, i[j]['telefono'], i[j]['contrasena'], i[j]['provincia'],
                       i[j]['permisos'],
                       i[j]['emails']['total'], i[j]['emails']['phishing'], i[j]['emails']['cliclados'], tb64(i[j]['fechas']), tb64(i[j]['ips']))
            lista.append(mytuple)
            #print(lista).
        c.executemany('INSERT OR IGNORE INTO users VALUES(?,?,?,?,?,?,?,?,?,?)', lista)
    conn.commit()
    conn.close()

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
              "permisos bool, emails_total integer , emails_phishing integer , emails_ciclados integer, fechas text, ips text, "
              "PRIMARY KEY(username))")

    conn.commit()
    return


def main():
    legal, users = leer_datos()
    insertar_datos(legal, users)
    create_dataframes()


if __name__ == '__main__':
    main()
