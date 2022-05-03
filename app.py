import pandas as pd
from flask import Flask, render_template, redirect, url_for, request, send_file, Response
from Entrega1.src.database import *
from Entrega1.src.Ejercicio4 import *
app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    x = request.args.get('n', default=10, type=int)
    c, conn = connect_db("Entrega1/database/database.db")
    df1 = pd.read_sql_query("select * from users", conn)
    df1 = porcentaje_peligro(df1)
    df1 = usuarios_criticos(df1).head(x)
    top_users_plot(df1)
    return render_template('pages/dashboard.html')

@app.route('/graphics/<id>', methods=['GET'])
def get_graphic(id):
    try:
        return send_file("Entrega1/graphics/"+id+".png")
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


if __name__ == '__main__':
    app.run(debug=True)
