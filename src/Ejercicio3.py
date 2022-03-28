import pandas as pd
from database import *


def count_missing(s: pd.Series):
    j = 0
    for i in s:
        if i:
            j += 1
    return j


def ejercicio3(df: pd.DataFrame, f):
    p0 = df.loc[df['permisos'] == 0]
    p1 = df.loc[df['permisos'] == 1]
    # print(p0)
    # print("Separador\n", df.loc[df['permisos'] == 0])
    print("USUARIOS CON PERMISO 0")
    f.write(f"USUARIOS CON PERMISO 0\n")
    print("Número de observaciones -> ", p0['emails_phishing'].sum())
    f.write(f"Número de observaciones -> {p0['emails_phishing'].sum()}\n")
    print("Número de valores ausentes -> ", p0['emails_phishing'].isna().sum())
    f.write(f"Número de valores ausentes -> {p0['emails_phishing'].isna().sum()}\n")
    print("Mediana -> ", p0['emails_phishing'].median())
    f.write(f"Mediana -> {p0['emails_phishing'].median()}\n")
    print("Media -> ", p0['emails_phishing'].mean())
    f.write(f"Media -> {p0['emails_phishing'].mean()}\n")
    print("Varianza -> ", p0['emails_phishing'].var())
    f.write(f"Varianza -> {p0['emails_phishing'].var()}\n")
    print("Valor máximo -> ", p0['emails_phishing'].max())
    f.write(f"Valor máximo -> {p0['emails_phishing'].max()}\n")
    print("Valor mínimo -> ", p0['emails_phishing'].min())
    f.write(f"Valor mínimo -> {p0['emails_phishing'].min()}\n\n")
    print("USUARIOS CON PERMISO 1")
    f.write(f"USUARIOS CON PERMISO 1\n")
    print("Número de observaciones -> ", p1['emails_phishing'].sum())
    f.write(f"Número de observaciones -> {p1['emails_phishing'].sum()}\n")
    print("Número de valores ausentes -> ", p1['emails_phishing'].isna().sum())
    f.write(f"Número de valores ausentes -> {p1['emails_phishing'].isna().sum()}\n")
    print("Mediana -> ", p1['emails_phishing'].median())
    f.write(f"Mediana -> {p1['emails_phishing'].median()}\n")
    print("Media -> ", p1['emails_phishing'].mean())
    f.write(f"Media -> {p1['emails_phishing'].mean()}\n")
    print("Varianza -> ", p1['emails_phishing'].var())
    f.write(f"Varianza -> {p1['emails_phishing'].var()}\n")
    print("Valor máximo -> ", p1['emails_phishing'].max())
    f.write(f"Valor máximo -> {p1['emails_phishing'].max()}\n")
    print("Valor mínimo -> ", p1['emails_phishing'].min())
    f.write(f"Valor mínimo -> {p1['emails_phishing'].min()}\n\n")


def ejercicio3_v2(df: pd.DataFrame, f):
    p0 = df.loc[df['emails_total'] < 200]
    p1 = df.loc[df['emails_total'] >= 200]
    # print(p0[['username','emails_total', 'emails_phishing']])
    # print(p1[['username','emails_total', 'emails_phishing']])
    print("MENOS DE 200 CORREOS")
    f.write("MENOS DE 200 CORREOS\n")
    print("Número de observaciones -> ", p0['emails_phishing'].sum())
    f.write(f"Número de observaciones -> {p0['emails_phishing'].sum()}\n")
    print("Número de valores ausentes -> ", p0['emails_phishing'].isna().sum())
    f.write(f"Número de valores ausentes -> {p0['emails_phishing'].isna().sum()}\n")
    print("Mediana -> ", p0['emails_phishing'].median())
    f.write(f"Mediana -> {p0['emails_phishing'].median()}\n")
    print("Media -> ", p0['emails_phishing'].mean())
    f.write(f"Media -> {p0['emails_phishing'].mean()}\n")
    print("Varianza -> ", p0['emails_phishing'].var())
    f.write(f"Varianza -> {p0['emails_phishing'].var()}\n")
    print("Valor máximo -> ", p0['emails_phishing'].max())
    f.write(f"Valor máximo -> {p0['emails_phishing'].max()}\n")
    print("Valor mínimo -> ", p0['emails_phishing'].min())
    f.write(f"Valor mínimo -> {p0['emails_phishing'].min()}\n\n")
    print("200 CORREOS O MÁS")
    f.write("200 CORREOS O MÁS\n")
    print("Número de observaciones -> ", p1['emails_phishing'].sum())
    f.write(f"Número de observaciones -> {p1['emails_phishing'].sum()}\n")
    print("Número de valores ausentes -> ", p1['emails_phishing'].isna().sum())
    f.write(f"Número de valores ausentes -> {p1['emails_phishing'].isna().sum()}\n")
    print("Mediana -> ", p1['emails_phishing'].median())
    f.write(f"Mediana -> {p1['emails_phishing'].median()}\n")
    print("Media -> ", p1['emails_phishing'].mean())
    f.write(f"Media -> {p1['emails_phishing'].mean()}\n")
    print("Varianza -> ", p1['emails_phishing'].var())
    f.write(f"Varianza -> {p1['emails_phishing'].var()}\n")
    print("Valor máximo -> ", p1['emails_phishing'].max())
    f.write(f"Valor máximo -> {p1['emails_phishing'].max()}\n")
    print("Valor mínimo -> ", p1['emails_phishing'].min())
    f.write(f"Valor mínimo -> {p1['emails_phishing'].min()}\n\n")

