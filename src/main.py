from database import generar_dataframes
from Ejercicio2 import ejercicio2
from Ejercicio3 import ejercicio3, ejercicio3_v2
from Ejercicio4 import ejercicio4

if __name__ == '__main__':
    df_usuarios, df_legal = generar_dataframes()
    ejercicio2(df_usuarios)
    ejercicio3(df_usuarios)
    ejercicio3_v2(df_usuarios)
    ejercicio4(df_usuarios, df_legal)
