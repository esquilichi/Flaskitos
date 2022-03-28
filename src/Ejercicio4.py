from database import *
import pandas as pd
import hashlib
import matplotlib.pyplot as plt


def lines_that_contain(string: str, fp):
    return [line for line in fp if string in line]

def porcentaje_peligro(df0: pd.DataFrame):
    # Esto lo que hace es crear una columna "porcentaje_click" en un nuevo dataframe para conocer los usuarios que mas
    # clican en emails de phishing
    for i, r in df0.iterrows():
        if r['emails_phishing'] != 0:
            df0._set_value(i, "porcentaje_click", r['emails_ciclados'] / r['emails_phishing'])
        else:
            df0._set_value(i, "porcentaje_click", 0)
    return df0.sort_values("porcentaje_click", ascending=False)


def usuarios_criticos(df0: pd.DataFrame):
    lines = open("../database/criticos.txt").read().splitlines()
    for i, r in df0.iterrows():
        if r['username'] in lines:
            df0._set_value(i, "critico", True)
        else:
            df0._set_value(i, "critico", False)
    return df0.sort_values(['critico', "porcentaje_click"], ascending=[False, False])


def get_all_hashes(df: pd.DataFrame):
    with open("../database/hashesonly.txt", "w") as f:
        for index, rows in df.iterrows():
            f.write(str(rows[3]))
            f.write("\n")

def crack_hashes():
    lista = list()
    u = open("../database/hashes.txt", "r").read().splitlines()
    criticos = open("../database/criticos.txt", "w")
    with open("../database/hashes.txt") as h:
        for i in h:
            lista.append(i.strip().split(":")[1])

    with open("../database/10000_passwords.txt") as f:
        for i in f.read().splitlines():
            linea = hashlib.md5(bytes(i, encoding='utf8'))
            if linea.hexdigest() in lista:
                criticos.write(lines_that_contain(linea.hexdigest(), u)[0].split(":")[0] + "\n")


def top_users_plot(df: pd.DataFrame):
    df.plot(x='username', y='emails_phishing', kind='bar')
    plt.show()

def get_paginas_desactualizadas(df: pd.DataFrame):
    for i, r in df.iterrows():
        df._set_value(i, 'n_politicas', r['cookies'] + r['aviso'] + r['proteccion_datos'])
    return df.sort_values(['n_politicas', 'creacion'], ascending=[False, True]).head(5)

def paginas_plot(df: pd.DataFrame):
    df.plot(x='url', y='creacion', kind='bar')
    plt.ylim((1990, 2022))
    plt.show()


def comprometidas_plot(comprometidas, no_comprometidas):
    fig = plt.figure(figsize = (10, 5))
    headers = ['Comprometidas', 'No Comprometidas']
    nu = [comprometidas, no_comprometidas]
    plt.bar(headers, nu, width=0.4)
    plt.title("Contraseñas comprometidas vs no comprometidas")
    plt.show()

def ejercicio4():
    _, conn = connect_db("../database/database.db")
    # Obtener todos los hashes de los usuarios
    # Punto 1
    df0 = pd.read_sql_query("SELECT username, emails_ciclados, emails_phishing, contrasena FROM users", conn)
    get_all_hashes(df0)
    crack_hashes()
    df1 = porcentaje_peligro(df0)
    df2 = usuarios_criticos(df1)
    top_users_plot(df2.head(10))

    # Punto 2
    legal0 = get_paginas_desactualizadas(pd.read_sql_query("SELECT * from legal", conn))
    paginas_plot(legal0)

    # Punto 3 TODO

    # Punto 4 TODO

    # Punto 5
    comprometidas = len(open("../database/criticos.txt").readlines())
    no_comprometidas = len(open("../database/hashes.txt").readlines()) - comprometidas
    comprometidas_plot(comprometidas, no_comprometidas)

    conn.close()


if __name__ == '__main__':
    ejercicio4()
