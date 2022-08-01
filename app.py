from flask import render_template, request, redirect, url_for, flash
import os
from flask import Flask, send_file
from flask_sqlalchemy import SQLAlchemy
from forms import *
from sqlalchemy.exc import IntegrityError
from skaiciavimai import kuno_mases_indeksas, bmr, intensyvumas, tikslas, maisto_svorio_maistingumas, \
    maistingumo_listo_suma
from flask_login import LoginManager, UserMixin, current_user, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Message, Mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from os import environ
from isbandymas import issukis1, issukis2, issukis3, atnaujinti


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bet kokia simbolių eilutė'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'registruotis'
login_manager.login_message_category = 'info'

bcrypt = Bcrypt(app)


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


class ManoModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.el_pastas == "rokas.prabusas@gmail.com"


admin = Admin(app)
admin.add_view(ManoModelView(Vartotojas, db.session))
admin.add_view(ManoModelView(Straipsnis, db.session))
admin.add_view(ManoModelView(Maistingumas, db.session))


@login_manager.user_loader
def load_user(vartotojo_id):
    return Vartotojas.query.get(int(vartotojo_id))


@app.route("/registruotis", methods=['GET', 'POST'])
def registruotis():
    db.create_all()
    form = RegistracijosForma()
    if form.validate_on_submit():
        try:
            koduotas_slaptazodis = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
            vartotojas = Vartotojas(vardas=form.vardas.data, el_pastas=form.el_pastas.data,
                                    slaptazodis=koduotas_slaptazodis)
            db.session.add(vartotojas)
            db.session.commit()
            flash('Sėkmingai prisiregistravote! Galite prisijungti', 'success')
        except IntegrityError:
            flash('Toks vartotojas jau yra!', 'danger')
    return render_template('registruotis.html', title='Register', form=form)


@app.route("/prisijungti", methods=['GET', 'POST'])
def prisijungti():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    form = PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('base'))
        else:
            flash('Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį', 'danger')
    return render_template('prisijungti.html', title='Prisijungti', form=form)


psw = environ.get('slaptazodis')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'rokas.prabusas058@gmail.com'
app.config['MAIL_PASSWORD'] = psw

mail = Mail(app)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Slaptažodžio atnaujinimo užklausa',
                  sender='el@pastas.lt',
                  recipients=[user.el_pastas])
    msg.body = f'''Norėdami atnaujinti slaptažodį, paspauskite nuorodą:
    {url_for('reset_token', token=token, _external=True)}
    Jei jūs nedarėte šios užklausos, nieko nedarykite ir slaptažodis nebus pakeistas.
    '''
    mail.send(msg)


@app.route("/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    form = UzklausosAtnaujinimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user is None:
            flash('Netinkamai įvestas el.paštas', 'danger')
            return render_template('reset_request.html', title='Reset Password', form=form)
        send_reset_email(user)
        flash('Jums išsiųstas el. laiškas su slaptažodžio atnaujinimo instrukcijomis.', 'info')
        return redirect(url_for('prisijungti'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    user = Vartotojas.verify_reset_token(token)
    if user is None:
        flash('Užklausa netinkama arba pasibaigusio galiojimo', 'warning')
        return redirect(url_for('reset_request'))
    form = SlaptazodzioAtnaujinimoForma()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        user.slaptazodis = hashed_password
        db.session.commit()
        flash('Tavo slaptažodis buvo atnaujintas! Gali prisijungti', 'success')
        return redirect(url_for('prisijungti'))
    return render_template('reset_token.html', title='Reset Password', form=form)


@app.route("/atsijungti")
def atsijungti():
    logout_user()
    return redirect(url_for('base'))


@app.route('/')
def base():
    return render_template('index.html')


@app.route('/maistas_prideti', methods=["GET", "POST"])
def maistas_prideti():
    form = PridejimoForma()
    if form.validate_on_submit():
        produktas = request.form.get('produktas').capitalize()
        kalorijos = int(request.form['kalorijos'])
        baltymai = float(request.form['baltymai'])
        angliavandeniai = float(request.form['angliavandeniai'])
        riebalai = float(request.form['riebalai'])
        prideti = Maistingumas(produktas, kalorijos, baltymai, angliavandeniai, riebalai)
        db.session.add(prideti)
        try:
            db.session.commit()
            flash('Sėkmingai pridėjote produktą!', 'success')
        except IntegrityError:
            db.session.rollback()
            flash('Toks produktas yra, patikrinkite!', 'danger')
    return render_template('maistas_prideti.html', form=form)


listas_maisto = []


@app.route('/tikrinti_maista', methods=['GET', 'POST'])
def tikrinti_maista():
    form = TikrintiForma()
    if request.method == 'POST' and form.validate_on_submit():
        produktas = request.form.get('ieskoti').capitalize()
        svoris = request.form.get('svoris')
        ieskoti = Maistingumas.query.filter_by(pavadinimas=produktas)
        surasta = ieskoti.all()
        if surasta == []:
            flash('Tokio produkto nėra arba blogai suvedėte!', 'danger')
            funkcija3 = maistingumo_listo_suma(listas_maisto)
            return render_template('tikrinti_maista.html', form=form, listas_maisto=listas_maisto, funkcija3=funkcija3)
        else:
            skaicius = len(listas_maisto)
            funkcija = maisto_svorio_maistingumas(svoris, surasta, skaicius)
            listas_maisto.append(funkcija)
            funkcija3 = maistingumo_listo_suma(listas_maisto)
            return render_template('tikrinti_maista.html', form=form, listas_maisto=listas_maisto,
                                   funkcija3=funkcija3)
    listas_maisto.clear()
    funkcija3 = maistingumo_listo_suma(listas_maisto)
    return render_template('tikrinti_maista.html', form=form, listas_maisto=listas_maisto, funkcija3=funkcija3)


@app.route('/kuno_mases_indeksas', methods=['GET', 'POST'])
def kmi():
    form = KalorijuForma()
    if request.method == 'POST' and form.validate_on_submit():
        mase = int(request.form['svoris'])
        ugis = int(request.form['ugis'])
        funkcija = kuno_mases_indeksas(ugis, mase)
        return render_template("kuno_mases_indeksas.html", form=form, funkcija=funkcija)
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


@app.route('/straipsniai_mityba')
def straipsniai_mityba():
    page = request.args.get('page', 1, type=int)
    data = Straipsnis.query.filter_by(tema="Mityba").order_by(Straipsnis.data.desc()).paginate(page=page, per_page=9)
    return render_template('straipsniai_mityba.html', data=data, datetime=datetime)


@app.route('/straipsniai_sportas')
def straipsniai_sportas():
    page = request.args.get('page', 1, type=int)
    data = Straipsnis.query.filter_by(tema="Sportas").order_by(Straipsnis.data.desc()).paginate(page=page, per_page=9)
    return render_template('straipsniai_sportas.html', data=data, datetime=datetime)


@app.route('/straipsniai_sveikata')
def straipsniai_sveikata():
    page = request.args.get('page', 1, type=int)
    data = Straipsnis.query.filter_by(tema="Sveikata").order_by(Straipsnis.data.desc()).paginate(page=page, per_page=9)
    return render_template('straipsniai_sveikata.html', data=data, datetime=datetime)


@app.route('/straipsniai_<string:tema>/<string:pavadinimas>#<int:id>')
def straipsnis(tema, pavadinimas, id):
    print(id)
    data = Straipsnis.query.filter_by(id=id)
    return render_template('straipsnis.html', pavadinimas=pavadinimas, tema=tema, id=id, data=data.all(),
                           datetime=datetime)


@app.route("/prideti_straipsni", methods=['GET', 'POST'])
@login_required
def prideti_straipsni():
    form = StraipsnisForma()
    if form.validate_on_submit():
        prideti = Straipsnis(vardas=current_user.vardas, pavadinimas=form.pavadinimas.data, tema=form.tema.data,
                             tekstas=form.tekstas.data)
        db.session.add(prideti)
        db.session.commit()
        flash('Sėkmingai įkeltas straipsnis!', 'success')
        if form.tema.data == "Mityba":
            return redirect(url_for('straipsniai_mityba'))
        if form.tema.data == "Sportas":
            return redirect(url_for('straipsniai_sportas'))
        if form.tema.data == "Sveikata":
            return redirect(url_for('straipsniai_sveikata'))
    return render_template('prideti_straipsni.html', title='prideti_straipsni', form=form)


@app.route("/issukis", methods=['GET', 'POST'])
@login_required
def issukis():
    form = IssukisForma()
    data = atnaujinti()
    if request.method == 'POST' and form.validate_on_submit():
        pasirinkimas = request.form.get('pasirinkimas')
        return redirect(url_for('atsisiusti', pasirinkimas=pasirinkimas))
    return render_template('issukis.html', form=form, data=data)


@app.route("/atsisiusti<string:pasirinkimas>")
@login_required
def atsisiusti(pasirinkimas):
    if pasirinkimas == "Lengvas":
        data = datetime.today().date()
        funkcija = issukis1(data)
        path = "issukis1"
        return send_file(path, as_attachment=True)
    if pasirinkimas == "Vidutinis":
        data = datetime.today().date()
        funkcija = issukis2(data)
        path = "issukis2"
        return send_file(path, as_attachment=True)
    if pasirinkimas == "Sunkus":
        data = datetime.today().date()
        funkcija = issukis3(data)
        path = "issukis3"
        return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
