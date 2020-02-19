from flask import Flask
from flask import render_template, request
from flask_migrate import Migrate, MigrateCommand
from flask_pymongo import PyMongo
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config['development'])

db = SQLAlchemy()
db.init_app(app)
mongo = PyMongo(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


class Citizen_EC(db.Model):
    __tablename__ = 'EC'
    __bind_key__ = 'postgres_bind'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80))
    address = db.Column(db.String(80))

    def __init__(self, full_name, address):
        self.full_name = full_name
        self.address = address

    def __repr__(self):
        return '<Full Name: {}>'.format(self.full_name)


class Citizen_GIS(db.Model):
    __tablename__ = 'GIS'
    __bind_key__ = 'mysql_bind'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80))
    address = db.Column(db.String(80))

    def __init__(self, full_name, address):
        self.full_name = full_name
        self.address = address

    def __repr__(self):
        return '<Full Name: {}>'.format(self.full_name)


class Citizen_NHIA(db.Model):
    __tablename__ = 'NHIS'
    __bind_key__ = 'sqlite_bind'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80))
    address = db.Column(db.String(80))

    def __init__(self, full_name, address):
        self.full_name = full_name
        self.address = address

    def __repr__(self):
        return '<Full Name: {}>'.format(self.full_name)


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []

    if request.method == "POST":
        full_name = request.form['full_name']

        if full_name:
            results_EC = Citizen_EC.query.filter_by(full_name=full_name).all()
            results_GIS = Citizen_GIS.query.filter_by(full_name=full_name).all()
            results_NHIA = Citizen_NHIA.query.filter_by(full_name=full_name).all()

            citizens = mongo.db.individual_DVLA
            results_DVLA_1 = []
            for c in citizens.find():
                results_DVLA_1.append(
                    {'full_name': c['full_name'], 'address': c['address']})

            results_DVLA = []
            for citizen in results_DVLA_1:
                if citizen['full_name'] == full_name:
                    results_DVLA.append(
                        {'full_name': citizen['full_name'], 'address': citizen['address']})

            return render_template('names.html', results_EC=results_EC, results_GIS=results_GIS,
                                   results_NHIA=results_NHIA, results_DVLA=results_DVLA)
        else:
            errors = {"error": "The request payload is not in JSON format"}

    return render_template('index.html', errors=errors)


@app.route('/results', methods=['GET', ])
def results():
    return render_template('names.html')


if __name__ == "__main__":
    app.run()
