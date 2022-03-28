import pandas as pd
from database import clist


def min_fechas(df: pd.DataFrame) -> int:
    i = len(df['fechas'][0])
    for j in df['fechas']:
        if len(j) < i:
            i = len(j)
    return i


def max_fechas(df: pd.DataFrame) -> int:
    i = len(df['fechas'][0])
    for j in df['fechas']:
        if len(j) > i:
            i = len(j)
    return i

def ejercicio2(df: pd.DataFrame):
    muestras = len(df) * len(df.columns)
    print("Muestras -> " + str(int(muestras) - int(df.isna().sum().sum())))
    #print("Media de fechas en las que se ha iniciado sesión -> " + str(len(df['fechas'].sum()) / len(df)))
    print("Media de fechas en las que se ha iniciado sesión -> ", clist(df['fechas']).mean())
    print("Desviación estandar de fechas en las que se ha iniciado sesión -> ", clist(df['fechas']).std())
    print("Desviación estándar del total de fechas en las que se han iniciado sesión (version grupby) -> " + str(df.groupby('username').count().std()[0]))
    #TODO Revisar las desviaciones estandar
    print("---- Desviacion estandar por usuario ----")
    print(clist(df['fechas']) / clist(df['fechas']).mean())
    print("-------------------------")
    #  print(df.keys())

    print("Provincias sin rellenar: ", df['provincia'].isna().sum())
    print("Media de emails recibidos -> ", (df['emails_total'].mean()))
    print("Desviación estándar de emails recibidos -> ", df['emails_total'].std())
    #print("Media de las IPS que se han detectado ->", clist(df['ips']).sum() / len(df))
    print("Media de las IPS que se han detectado ->", clist(df['ips']).mean())
    print("Desviación estandar de las IPS que se han detectado ->", clist(df['ips']).std())
    #  print("Desviación estándar de emails recibidos -> ", np.std(df['emails_total'].to_numpy())) da un valor ligeramente distinto
    print("Valor mínimo del total de fechas que se ha inciado sesión -> ", min_fechas(df))
    print("Valor máximo del total de fechas que se ha iniciado sesión -> ", max_fechas(df))
    print("Valor mínimo del número de emails recibidos -> ", df['emails_total'].min())
    print("Valor mínimo del número de emails recibidos -> ", df['emails_total'].max())