import pandas as pd
from database import *


def count_missing(s: pd.Series):
    j = 0
    for i in s:
        if i:
            j += 1
    return j


def ejercicio3(df: pd.DataFrame):
    p0 = df.loc[df['permisos'] == 0]
    p1 = df.loc[df['permisos'] == 1]
    # print(p0)
    # print("Separador\n", df.loc[df['permisos'] == 0])
    print("USUARIOS CON PERMISO 0")
    print("Número de observaciones → ", p0['emails_phishing'].sum())
    print("Número de valores ausentes → ", count_missing(p0['emails_phishing'].isna()))
    print("Mediana → ", p0['emails_phishing'].median())
    print("Media → ", p0['emails_phishing'].mean())
    print("Varianza → ", p0['emails_phishing'].var())
    print("Valor máximo → ", p0['emails_phishing'].max())
    print("Valor mínimo → ", p0['emails_phishing'].min())
    print()
    print("USUARIOS CON PERMISO 1")
    print("Número de observaciones → ", p1['emails_phishing'].sum())
    print("Número de valores ausentes → ", count_missing(p1['emails_phishing'].isna()))
    print("Mediana → ", p1['emails_phishing'].median())
    print("Media → ", p1['emails_phishing'].mean())
    print("Varianza → ", p1['emails_phishing'].var())
    print("Valor máximo → ", p1['emails_phishing'].max())
    print("Valor mínimo → ", p1['emails_phishing'].min())
    print()


def ejercicio3_v2(df: pd.DataFrame):
    p0 = df.loc[df['emails_total'] < 200]
    p1 = df.loc[df['emails_total'] >= 200]
    # print(p0[['username','emails_total', 'emails_phishing']])
    # print(p1[['username','emails_total', 'emails_phishing']])
    print("MENOS DE 200 CORREOS")
    print("Número de observaciones → ", p0['emails_phishing'].sum())
    print("Número de valores ausentes → ", count_missing(p0['emails_phishing'].isna()))
    print("Mediana → ", p0['emails_phishing'].median())
    print("Media → ", p0['emails_phishing'].mean())
    print("Varianza → ", p0['emails_phishing'].var())
    print("Valor máximo → ", p0['emails_phishing'].max())
    print("Valor mínimo → ", p0['emails_phishing'].min())
    print()
    print("MENOS DE 200 CORREOS")
    print("Número de observaciones → ", p1['emails_phishing'].sum())
    print("Número de valores ausentes → ", count_missing(p1['emails_phishing'].isna()))
    print("Mediana → ", p1['emails_phishing'].median())
    print("Media → ", p1['emails_phishing'].mean())
    print("Varianza → ", p1['emails_phishing'].var())
    print("Valor máximo → ", p1['emails_phishing'].max())
    print("Valor mínimo → ", p1['emails_phishing'].min())

