import pandas as pd
from database import *


def count_missing(s: pd.Series):
    j = 0
    for i in s:
        if i:
            j += 1
    return j


def ejercicio3():
    _, conn = connect_db("../database/database.db")
    p0 = pd.read_sql_query("SELECT * FROM users WHERE permisos = 0", conn)
    p1 = pd.read_sql_query("SELECT * FROM users WHERE permisos = 1", conn)
    conn.close()
    print("USUARIOS CON PERMISO 0")
    print("Número de observaciones -> ", p0['emails_phishing'].sum())
    print("Número de valores ausentes -> ", count_missing(p0['emails_phishing'].isna()))
    print("Mediana -> ", p0['emails_phishing'].median())
    print("Media -> ", p0['emails_phishing'].mean())
    print("Varianza -> ", p0['emails_phishing'].var())
    print("Valor máximo -> ", p0['emails_phishing'].max())
    print("Valor mínimo -> ", p0['emails_phishing'].min())
    print()
    print("USUARIOS CON PERMISO 1")
    print("Número de observaciones -> ", p1['emails_phishing'].sum())
    print("Número de valores ausentes -> ", count_missing(p1['emails_phishing'].isna()))
    print("Mediana -> ", p1['emails_phishing'].median())
    print("Media -> ", p1['emails_phishing'].mean())
    print("Varianza -> ", p1['emails_phishing'].var())
    print("Valor máximo -> ", p1['emails_phishing'].max())
    print("Valor mínimo -> ", p1['emails_phishing'].min())


if __name__ == '__main__':
    ejercicio3()
