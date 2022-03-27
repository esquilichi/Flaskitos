from database import *
import pandas as pd
import hashlib

def lines_that_contain(string: str, fp):
    return [line for line in fp if string in line]


def get_all_hashes(df: pd.DataFrame):
    with open("../database/hashesonly.txt", "w") as f:
        for index, rows in df.iterrows():
            f.write(str(rows[3]))
            f.write("\n")

def crack_hashes():
    lista = list()
    u = open("../database/hashes.txt", "r").read().splitlines()

    with open("../database/hashes.txt") as h:
        for i in h:
            lista.append(i.strip().split(":")[1])

    with open("../database/10000_passwords.txt") as f:
        for i in f.read().splitlines():
            linea = hashlib.md5(bytes(i, encoding='utf8'))
            if linea.hexdigest() in lista:
                print(lines_that_contain(linea.hexdigest(), u)[0].split(":")[0])


def ejercicio4():
    _, conn = connect_db("../database/database.db")
    # Obtener todos los hashes de los usuarios
    df0 = pd.read_sql_query("SELECT username, emails_ciclados, emails_phishing, contrasena FROM users", conn)
    get_all_hashes(df0)
    crack_hashes()


if __name__ == '__main__':
    ejercicio4()
