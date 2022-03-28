from database import generar_dataframes
from Ejercicio2 import ejercicio2
from Ejercicio3 import ejercicio3, ejercicio3_v2
from Ejercicio4 import ejercicio4

if __name__ == '__main__':
    df_usuarios, df_legal = generar_dataframes()
    with open('../respuestas.txt', 'w') as sols:
        sols.write("Ismael Gomez, Adriano Campos, Alejandro Gallego\nGrupo R\nPractica 1\nEstas son las respuestas obtenidas para cada uno de los apartados de la practica:\n")
        sols.write("------Ejercicio 2------\n\n")
        ejercicio2(df_usuarios, sols)
        sols.write("----Fin del ejercicio 2----\n")
        sols.write("------Ejercicio 3------\n\n")
        ejercicio3(df_usuarios, sols)
        ejercicio3_v2(df_usuarios, sols)
        sols.write("----Fin del ejercicio 3----\n")
        ejercicio4(df_usuarios, df_legal)
        sols.close()
