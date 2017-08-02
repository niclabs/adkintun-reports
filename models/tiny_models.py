from app.app import db

class Person(db.Model):
    __tablename__ = 'useless'
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column('nombre', db.String(10))
    apellido = db.Column('apellido', db.String(10))
    edad = db.Column('edad', db.Integer)

    def __init__(self, un_id, un_nombre, un_apellido, una_edad):
        self.id = un_id
        self.nombre = un_nombre
        self.apellido = un_apellido
        self.edad = una_edad

class VIP(db.Model):
    __tablename__ = 'useful'
    __bind_key__ = 'everything'
    id = db.Column('id', db.Integer, primary_key=True)
    nombre = db.Column('nombre', db.String(10))
    apellido = db.Column('apellido', db.String(10))
    edad = db.Column('edad', db.Integer)

    def __init__(self, un_id, un_nombre, un_apellido, una_edad):
        self.id = un_id
        self.nombre = un_nombre
        self.apellido = un_apellido
        self.edad = una_edad
