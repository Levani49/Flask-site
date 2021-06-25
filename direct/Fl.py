from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'Cars.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)


class Vehicles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carName = db.Column(db.String(254), nullable=False)
    carType = db.Column(db.String(254), nullable=False)
    carModel = db.Column(db.String(254), nullable=False)
    color = db.Column(db.String(254), nullable=False)
    makeYear = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)


def insert_data(_request):
    vehicle = Vehicles(carName=_request.form['carname'],
                       carType=_request.form['cartype'],
                       carModel=_request.form['carmodel'],
                       color=_request.form['color'],
                       makeYear=int(_request.form['makeyear']),
                       price=int(_request.form['price']))

    db.session.add(vehicle)
    db.session.commit()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        userName = request.form['userName']
        session['username'] = userName
        return redirect(url_for('user', name=userName))

    return render_template('login.html')


@app.route('/<name>')
def user(name):
    if request.method == 'POST':
        return redirect(url_for('Machines.html'))
    else:
        return render_template('user.html')


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for("home"))


@app.route('/Machines', methods=['GET', 'POST'])
def Machines():
    if request.method == "POST":
        insert_data(request)
        flash('მონაცემები წარმატებით დაემატა')
        return redirect(url_for('Machines'))
    return render_template('Machines.html')


if __name__ == '__main__':
    app.run(debug=True)
