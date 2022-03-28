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

def ejercicio2(df: pd.DataFrame, f):
    muestras = len(df) * len(df.columns)
    print("Muestras -> " + str(int(muestras) - int(df.isna().sum().sum())))
    f.write(f"Muestras -> {str(int(muestras) - int(df.isna().sum().sum()))}\n" )
    #print("Media de fechas en las que se ha iniciado sesión -> " + str(len(df['fechas'].sum()) / len(df)))
    print("Media de fechas en las que se ha iniciado sesión -> ", clist(df['fechas']).mean())
    f.write(f"Media de fechas en las que se ha iniciado sesión -> {clist(df['fechas']).mean()}\n")
    print("Desviación estandar de fechas en las que se ha iniciado sesión -> ", clist(df['fechas']).std())
    f.write(f"Desviación estandar de fechas en las que se ha iniciado sesión -> {clist(df['fechas']).std()}\n")
    print("Desviación estándar del total de fechas en las que se han iniciado sesión (version grupby) -> " + str(df.groupby('username').count().std()[0]))
    f.write(f"Desviación estándar del total de fechas en las que se han iniciado sesión (version grupby) -> {str(df.groupby('username').count().std()[0])}\n")
    #TODO Revisar las desviaciones estandar
    # print("---- Desviacion estandar por usuario ----")
    # print(clist(df['fechas']) / clist(df['fechas']).mean())
    # print("-------------------------")
    #  print(df.keys())

    print("Provincias sin rellenar: ", df['provincia'].isna().sum())
    f.write(f"Provincias sin rellenar: {df['provincia'].isna().sum()}\n")
    print("Media de emails recibidos -> ", (df['emails_total'].mean()))
    f.write(f"Media de emails recibidos -> {(df['emails_total'].mean())}\n")
    print("Desviación estándar de emails recibidos -> ", df['emails_total'].std())
    f.write(f"Desviación estándar de emails recibidos -> {df['emails_total'].std()}\n")
    #print("Media de las IPS que se han detectado ->", clist(df['ips']).sum() / len(df))
    print("Media de las IPS que se han detectado ->", clist(df['ips']).mean())
    f.write(f"Media de las IPS que se han detectado -> {clist(df['ips']).mean()}\n")
    print("Desviación estandar de las IPS que se han detectado ->", clist(df['ips']).std())
    f.write(f"Desviación estandar de las IPS que se han detectado -> {clist(df['ips']).std()}\n")
    #  print("Desviación estándar de emails recibidos -> ", np.std(df['emails_total'].to_numpy())) da un valor ligeramente distinto
    print("Valor mínimo del total de fechas que se ha inciado sesión -> ", min_fechas(df))
    f.write(f"Valor mínimo del total de fechas que se ha inciado sesión -> {min_fechas(df)}\n")
    print("Valor máximo del total de fechas que se ha iniciado sesión -> ", max_fechas(df))
    f.write(f"Valor máximo del total de fechas que se ha iniciado sesión -> {max_fechas(df)}\n")
    print("Valor mínimo del número de emails recibidos -> ", df['emails_total'].min())
    f.write(f"Valor mínimo del número de emails recibidos -> {df['emails_total'].min()}\n")
    print("Valor mínimo del número de emails recibidos -> ", df['emails_total'].max())
    f.write(f"Valor mínimo del número de emails recibidos -> {df['emails_total'].max()}\n\n")