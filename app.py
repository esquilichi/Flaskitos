from datetime import datetime

import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, send_file, Response
import os
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from Entrega1.src.database import *
from Entrega1.src.Ejercicio4 import *
import requests
import feedparser
import plotly
import plotly.graph_objects as go
import plotly.express as px
import sqlite3


app = Flask(__name__)

con = sqlite3.connect('./database/flaskitos.db')
cursor = con.cursor()


def init_database():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users_flaskitos(user_id INT, username VARCHAR(250), passwordHash VARCHAR(250))""")



def get_driver():
    # Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
    profile = webdriver.FirefoxProfile()
    webdriver_options = FirefoxOptions()
    webdriver_options.add_argument("--headless")
    webdriver_options.add_argument("--disable-extensions")
    webdriver_options.add_argument("--no-sandbox")
    webdriver_options.add_argument("--disable-application-cache")
    webdriver_options.add_argument("--disable-gpu")
    webdriver_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(options=webdriver_options, firefox_profile=profile, log_path=os.path.devnull)
    return driver


def tratar_dataframe(df: pd.DataFrame, b: bool):
    if not b:
        df = df.loc[df['porcentaje_click'] < 50]
    return df


@app.route('/')
def hello_world():
    return redirect(url_for('dashboard'))


@app.route('/dashboard')
def dashboard():
    l = ejercicio4()
    exploit_list = exploitdb()
    x = request.args.get('n', default=10, type=int)
    critico = request.args.get('critico', default=True, type=bool)
    print(x, critico)
    c, conn = connect_db("Entrega1/database/database.db")
    df1 = pd.read_sql_query("select * from users", conn)
    df1 = porcentaje_peligro(df1)
    df1 = usuarios_criticos(df1).head(x)
    df1 = tratar_dataframe(df1, critico)
    top_users_plot(df1)
    data = plotlyF(df1)
    return render_template('pages/dashboard.html', item=l, exploits=exploit_list, data=data)


@app.route('/graphics/<id>', methods=['GET'])
def get_graphic(id):
    try:
        return send_file("Entrega1/graphics/" + id + ".png")
    except Exception as e:
        return str(e)


@app.route('/users/<id>', methods=['GET'])
def get_datajotason(id):
    try:
        c, conn = connect_db("Entrega1/database/database.db")
        df1 = pd.read_sql_query("select * from users", conn)
        df1 = porcentaje_peligro(df1)
        df1 = usuarios_criticos(df1)
        return Response(df1.to_json(orient='index'), mimetype='application/json')
    except Exception as e:
        return str(e)


def plotlyF(df: pd.DataFrame):
    trace = go.Bar(x=df["username"], y=df["porcentaje_click"])
    layout = go.Layout(title="Top usuarios críticos", xaxis=dict(title="username"),
                       yaxis=dict(title="porcentaje_click"))
    data = [trace]
    fig = go.Figure(data=data, layout=layout)
    fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return fig_json


def ejercicio4():
    r = requests.get("https://cve.circl.lu/api/last")
    jotason = json.loads(r.text)
    l = []
    for i in range(10):
        temp = jotason[i]
        l.append(temp)
    return l


def exploitdb():
    exploitdb_list = []
    last_exploitdb = feedparser.parse("https://www.exploit-db.com/rss.xml")
    for article in last_exploitdb.entries:
        name = article.description
        link = article.link
        category = article.title.split("]")[0][1:]
        exploitdb_list.append({"name": name, "category": category, "link": link, "saved": False})
    return exploitdb_list


if __name__ == '__main__':
    init_database()
    app.run(debug=True)
