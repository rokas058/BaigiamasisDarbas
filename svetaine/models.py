from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from svetaine import app, db


class Maistingumas(db.Model):
    __tablename__ = 'maistingumas'
    id = db.Column(db.Integer, primary_key=True)
    pavadinimas = db.Column(db.String(80), unique=True, nullable=False)
    kalorijos = db.Column(db.Integer, nullable=False)
    baltymai = db.Column(db.Float, nullable=False)
    angliavandeniai = db.Column(db.Float, nullable=False)
    riebalai = db.Column(db.Float, nullable=False)

    def __init__(self, pavadinimas, kalorijos, baltymai, angliavandeniai, riebalai):
        self.pavadinimas = pavadinimas
        self.kalorijos = kalorijos
        self.baltymai = baltymai
        self.angliavandeniai = angliavandeniai
        self.riebalai = riebalai

    def __repr__(self):
        return f'{self.pavadinimas} : {self.kalorijos}, {self.baltymai}, {self.angliavandeniai}, {self.riebalai}'


class Vartotojas(db.Model, UserMixin):
    __tablename__ = "vartotojas"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String(20), unique=True, nullable=False)
    el_pastas = db.Column("El. pašto adresas", db.String(120), unique=True, nullable=False)
    slaptazodis = db.Column("Slaptažodis", db.String(60), unique=True, nullable=False)

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Vartotojas.query.get(user_id)


class Straipsnis(db.Model):
    __tablename__ = "straipsnis"
    id = db.Column(db.Integer, primary_key=True)
    vardas = db.Column("Vardas", db.String(), nullable=False)
    pavadinimas = db.Column("Pavadinimas", db.String(), nullable=False)
    tema = db.Column("Tema", db.String(), nullable=False)
    data = db.Column("Data", db.DateTime(), nullable=False, default=datetime.today())
    tekstas = db.Column("Tekstas", db.String(), nullable=False)

    def __repr__(self):
        return f'{self.vardas}, {self.pavadinimas}, {self.tema}, {self.data}, {self.tekstas}'