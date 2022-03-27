from database import *
import pandas as pd


def get_all_hashes(df: pd.DataFrame):
    with open("../database/hashes.txt", "w") as f:
        for index, rows in df.iterrows():
            f.write(str(rows[0]) + ":" + str(rows[3]))
            f.write("\n")


def ejercicio4():
    _, conn = connect_db("../database/database.db")
    # Obtener todos los hashes de los usuarios
    df0 = pd.read_sql_query("SELECT username, emails_ciclados, emails_phishing, contrasena FROM users", conn)
    get_all_hashes(df0)


if __name__ == '__main__':
    ejercicio4()
