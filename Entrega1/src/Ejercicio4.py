import numpy as np
import pandas as pd
import hashlib
import matplotlib.pyplot as plt

clist = lambda x: x.str.len()  #Conversor de listas a n elementos

def lines_that_contain(string: str, fp) -> list:
    return [line for line in fp if string in line]

def porcentaje_peligro(df0: pd.DataFrame) -> pd.DataFrame:
    # Esto lo que hace es crear una columna "porcentaje_click" en un nuevo dataframe para conocer los usuarios que mas
    # clican en emails de phishing
    for i, r in df0.iterrows():
        if r['emails_phishing'] != 0:
            df0._set_value(i, "porcentaje_click", r['emails_ciclados'] / r['emails_phishing']*100)
        else:
            df0._set_value(i, "porcentaje_click", 0)
    return df0.sort_values("porcentaje_click", ascending=False)


def usuarios_criticos(df0: pd.DataFrame) -> pd.DataFrame:
    lines = open("Entrega1/database/criticos.txt").read().splitlines()
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
    df.plot(x='username', y='porcentaje_click', kind='bar', figsize=(12.8, 7.2))
    plt.title('Top 10 usuarios críticos según su porcentaje de clicks en phising', loc='left')
    plt.ylim((0,100))
    plt.xlabel('Usuarios')
    plt.ylabel('% de clicks en phising')
    plt.savefig("static/assets/graficos/users.png")

def get_paginas_desactualizadas(df: pd.DataFrame):
    for i, r in df.iterrows():
        df._set_value(i, 'n_politicas', r['cookies'] + r['aviso'] + r['proteccion_datos'])
    print(df.sort_values(['n_politicas', 'creacion'], ascending=[True, True]).head(5))
    return df.sort_values(['n_politicas', 'creacion'], ascending=[True, True]).head(5)

def paginas_plot(df: pd.DataFrame):
    df.plot(x='url', y='n_politicas', kind='bar',figsize=(12.8, 7.2))
    plt.ylim((0, 4))
    plt.title('Top 5 paginas web con más políticas desactualizadas', loc='left')
    plt.xlabel('Sitios web')
    plt.ylabel('Número de políticas')
    plt.savefig('../graphics/4-2.png', dpi=400)
    plt.show()


def comprometidas_plot(comprometidas: list, no_comprometidas: list):
    fig = plt.figure(figsize=(12.8, 7.2))
    headers = ['Comprometidas', 'No Comprometidas']
    nu = [comprometidas, no_comprometidas]
    plt.title("Contraseñas comprometidas vs no comprometidas", loc='left')
    plt.pie(nu, labels=headers, autopct=lambda _: f"{int((_/100)*(comprometidas + no_comprometidas))}", colors=["#40D4FF", "#FEDD23"])
    plt.axis("equal")
    plt.savefig('../graphics/4-5.png', dpi=400)
    plt.show()

def conexiones_usuario(df: pd.DataFrame):
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
    print("Inicios de no criticos respecto inicios totales", no_criticos / total * 100, "%")
    fig = plt.figure(figsize=(12.8, 7.2))
    headers = ['Inicios de sesion de cuentas criticas', 'Inicios de sesion de cuentas no criticas']
    nu = [counter_criticos, no_criticos]
    plt.pie(nu, labels=headers, autopct=lambda _: f"{_:0.2f}% ({int((_/100)*(counter_criticos + no_criticos))})", colors=["#FD1E0F", "#3EFA02"], explode=(0,0.1))
    plt.axis("equal")
    plt.title("Porcentaje de inicios de sesión de criticos y no criticos", loc='left')
    plt.savefig('../graphics/4-3.png', dpi=400)
    plt.show()

def comparativa_porano(df: pd.DataFrame):
    print("Tabla completa:")
    print(df.groupby('creacion').value_counts())
    anos = (df.groupby('creacion').groups.keys())
    i = int(-1)
    cumplen = []
    nocumplen = []
    lastyear = int(-9999999)
    for el in df.groupby('creacion').value_counts().iteritems():
        if lastyear != el[0][0]:
            lastyear = el[0][0]
            i += 1
            cumplen.append(0)
            nocumplen.append(0)
        if el[0][2] == 1 and el[0][3] == 1 and el[0][4] == 1:
            cumplen[i] += 1
        else:
            nocumplen[i]+=1

    index_barras = np.arange(len(anos))
    ancho = 0.35
    plt.figure(figsize=(12.8, 7.2))
    plt.bar(index_barras, cumplen, width=ancho, label='Sitios que cumplen')
    plt.bar(index_barras + ancho, nocumplen, width=ancho, label='Sitios que no cumplen')
    plt.legend(loc='best')
    plt.xticks(index_barras+(ancho/2), anos)
    print(max(cumplen + nocumplen))
    plt.yticks(np.arange(0, max(cumplen + nocumplen) + 2))# +2→ 1 para incluir el maximo, otro por estetica
    plt.xlabel('Años')
    plt.ylabel('Sitios')
    plt.title('Comparativa de webs que cumplían con las políticas de privacidad por año', loc='left')
    plt.savefig('../graphics/4-4.png', dpi=400)
    plt.show()




def ejercicio4(df: pd.DataFrame, df_legal: pd.DataFrame):
    # Obtener todos los hashes de los usuarios
    # Punto 1
    get_all_hashes(df)
    crack_hashes()
    df1 = porcentaje_peligro(df)
    df2 = usuarios_criticos(df1)
    print(df2)
    top_users_plot(df2.head(10))

    # Punto 2
    legal0 = get_paginas_desactualizadas(df_legal)
    paginas_plot(legal0)

    # Punto 3
    conexiones_usuario(df)

    # Punto 4
    comparativa_porano(df_legal)

    # Punto 5
    comprometidas = len(open("../database/criticos.txt").readlines())
    no_comprometidas = len(open("../database/hashes.txt").readlines()) - comprometidas
    comprometidas_plot(comprometidas, no_comprometidas)




