from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('pages/dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)
