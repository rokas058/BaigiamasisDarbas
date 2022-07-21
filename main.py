from flask import Flask, render_template, request
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from forms import *
from sqlalchemy.exc import IntegrityError


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bet kokia simbolių eilutė'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/maistas_prideti', methods=["GET", "POST"])
def maistas_prideti():
        form = PridejimoForma()
        if form.validate_on_submit():
            try:
                produktas = request.form.get('produktas').capitalize()
                kalorijos = int(request.form['kalorijos'])
                baltymai = float(request.form['baltymai'])
                angliavandeniai = float(request.form['angliavandeniai'])
                riebalai = float(request.form['riebalai'])
                prideti = Maistingumas(produktas, kalorijos, baltymai, angliavandeniai, riebalai)
                db.session.add(prideti)
                db.session.commit()
            except IntegrityError:
                return render_template('klaida.html')
            return render_template('pridetas_produktas.html', form=form)
        return render_template('maistas_prideti.html', form=form)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
