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
    with open("../database/10000_passwords.txt", encoding='utf8') as f:
        for i in f.read().splitlines():
            linea = hashlib.md5(bytes(i, encoding='utf8'))
            if linea.hexdigest() in lista:
                criticos.write(lines_that_contain(linea.hexdigest(), u)[0].split(":")[0] + "\n")



def top_users_plot(df: pd.DataFrame):
    df.plot(x='username', y='emails_phishing', kind='bar', figsize=(12.8, 7.2))
    plt.show()

def get_paginas_desactualizadas(df: pd.DataFrame):
    for i, r in df.iterrows():
        df._set_value(i, 'n_politicas', r['cookies'] + r['aviso'] + r['proteccion_datos'])
    return df.sort_values(['n_politicas', 'creacion'], ascending=[False, True]).head(5)

def paginas_plot(df: pd.DataFrame):
    df.plot(x='url', y='creacion', kind='bar',figsize=(12.8, 7.2))
    plt.ylim((1990, 2022))
    plt.show()


def comprometidas_plot(comprometidas, no_comprometidas):
    fig = plt.figure(figsize=(12.8, 7.2))
    headers = ['Comprometidas', 'No Comprometidas']
    nu = [comprometidas, no_comprometidas]
    plt.bar(headers, nu, width=0.4)
    plt.title("Contraseñas comprometidas vs no comprometidas")
    plt.show()

def conexiones_usuario(df: pd.DataFrame):
    df['fechas'] = df['fechas'].apply(fb64)
    df['n_conexiones'] = clist(df['fechas'])
    total = df['n_conexiones'].sum()
    counter_criticos = int(0)
    with open('../database/criticos.txt') as f:
        for line in f:
            name = line.strip('\n')
            user = df.loc[df['username'] == name, 'n_conexiones']
            #print(user)
            #print(user.values[0])
            counter_criticos += int(user.values[0])
    print("Inicios sesion criticos", counter_criticos)
    no_criticos = total - counter_criticos
    print("Inicios de sesion no criticos", no_criticos)
    print("Inicios de criticos respecto inicios totales", counter_criticos / total * 100, "%")
    porcentaje_criticos = counter_criticos / total * 100
    porcentaje_ncriticos = no_criticos / total * 100
    print("Inicios de criticos respecto inicios totales", no_criticos / total * 100, "%")
    fig = plt.figure(figsize=(12.8, 7.2))
    headers = ['Inicios de sesion criticos', 'Inicios de sesion no criticos']
    nu = [porcentaje_criticos, porcentaje_ncriticos]
    plt.bar(headers, nu, width=0.4)
    plt.title("Porcentaje de inicios de sesión de criticos y no criticos")
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

    # Punto 3 TODO Revisar entre todos el tema de los porcentajes
    df3 = pd.read_sql_query("SELECT username, fechas from users", conn)
    conexiones_usuario(df3)

    # Punto 4 TODO

    # Punto 5
    comprometidas = len(open("../database/criticos.txt").readlines())
    no_comprometidas = len(open("../database/hashes.txt").readlines()) - comprometidas
    comprometidas_plot(comprometidas, no_comprometidas)

    conn.close()


if __name__ == '__main__':
    ejercicio4()
