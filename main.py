from flask import Flask, render_template, request, redirect
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from forms import *
from sqlalchemy.exc import IntegrityError


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bet kokia simbolių eilutė'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

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
            return render_template('klaida.html', form=form)
        return render_template('pridetas_produktas.html', form=form)
    return render_template('maistas_prideti.html', form=form)


@app.route('/tikrinti_maista', methods=['GET', 'POST'])
def tikrinti_maista():
    form = TikrintiForma()
    if request.method == 'POST' and form.validate_on_submit():
        produktas = request.form.get('ieskoti').capitalize()
        ieskoti = Maistingumas.query.filter_by(pavadinimas=produktas)
        surasta = ieskoti.all()
        if surasta == []:
            nera = "Nerastas produktas"
            return render_template('tikrinti_maista.html', form=form, nera=nera)
        return render_template('tikrinti_maista.html', form=form, surasta=surasta)
    return render_template('tikrinti_maista.html', form=form)


from skaiciavimai import kuno_mases_indeksas, bmr, intensyvumas, tikslas


@app.route('/kuno_mases_indeksas', methods=['GET', 'POST'])
def kmi():
    form = KalorijuForma()
    if request.method == 'POST' and form.validate_on_submit():
        mase = int(request.form['svoris'])
        ugis = int(request.form['ugis'])
        funkcija = kuno_mases_indeksas(ugis, mase)
        atsakymas1 = funkcija[0]
        atsakymas2 = funkcija[1]
        return render_template("kuno_mases_indeksas.html", form=form, atsakymas1=atsakymas1, atsakymas2=atsakymas2)
    return render_template("kuno_mases_indeksas.html", form=form)


@app.route('/dienos_kaloriju_norma', methods=['GET', 'POST'])
def dkn():
    form = DienosKalorijuForma()
    if request.method == 'POST' and form.validate_on_submit():
        mase = int(request.form['svoris'])
        ugis = int(request.form['ugis'])
        amzius = int(request.form['amzius'])
        lytis = request.form['lytis']
        daznumas = request.form["intensyvumas"]
        funkcija1 = bmr(mase, ugis, amzius, lytis)
        funkcija2 = intensyvumas(daznumas, funkcija1)
        rezultatas = tikslas(funkcija2)
        return render_template('dienos_kaloriju_norma.html', form=form, rezultatas=rezultatas)
    return render_template('dienos_kaloriju_norma.html', form=form)


@app.route('/kojoms')
def kojoms():
    return render_template('kojoms.html')


@app.route('/nugarai')
def nugarai():
    return render_template('nugarai.html')


@app.route('/presui')
def presui():
    return render_template('presui.html')


@app.route('/rankoms')
def rankoms():
    return render_template('rankoms.html')


@app.route('/peciams')
def peciams():
    return render_template('peciams.html')


@app.route('/krutinei')
def krutinei():
    return render_template('krutinei.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
