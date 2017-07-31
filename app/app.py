from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# modelo de prueba
class Useless(db.Model):
    __tablename__ = 'useless'
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column('nombre', db.String(10))
    apellido = db.Column('apellido', db.String(10))
    edad = db.Column('edad', db.String(10))

class Useful(db.Model):
    __tablename__ = 'useful'
    __bind_key__ = 'everything'
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column('nombre', db.String(10))
    apellido = db.Column('apellido', db.String(10))
    edad = db.Column('edad', db.String(10))
