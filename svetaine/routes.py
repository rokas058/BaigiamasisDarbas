from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime
from flask_mail import Message
from svetaine import forms, db, app, bcrypt, mail
from svetaine.models import Vartotojas, Straipsnis, Maistingumas
from sqlalchemy.exc import IntegrityError
from svetaine.skaiciavimai import maistingumo_listo_suma, maisto_svorio_maistingumas, kuno_mases_indeksas, intensyvumas, bmr, \
    tikslas
from svetaine.isbandymas import atnaujinti, issukis1, issukis2, issukis3
from flask import send_file


@app.route("/registruotis", methods=['GET', 'POST'])
def registruotis():
    db.create_all()
    form = forms.RegistracijosForma()
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
    form = forms.PrisijungimoForma()
    if form.validate_on_submit():
        user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
        if user and bcrypt.check_password_hash(user.slaptazodis, form.slaptazodis.data):
            login_user(user, remember=form.prisiminti.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('base'))
        else:
            flash('Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį', 'danger')
    return render_template('prisijungti.html', title='Prisijungti', form=form)


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
        user_current = Vartotojas.query.filter_by(el_pastas=current_user.el_pastas).first()
        send_reset_email(user_current)
        flash('Jums išsiųstas el. laiškas su slaptažodžio atnaujinimo instrukcijomis.', 'info')
        return redirect(url_for('base'))
    form = forms.UzklausosAtnaujinimoForma()
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
    user = Vartotojas.verify_reset_token(token)
    if user is None:
        flash('Užklausa netinkama arba pasibaigusio galiojimo', 'warning')
        return redirect(url_for('reset_request'))
    form = forms.SlaptazodzioAtnaujinimoForma()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.slaptazodis.data).decode('utf-8')
        user.slaptazodis = hashed_password
        db.session.commit()
        flash('Tavo slaptažodis buvo atnaujintas!', 'success')
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
    db.create_all()
    form = forms.PridejimoForma()
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
    db.create_all()
    form = forms.TikrintiForma()
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
    form = forms.KalorijuForma()
    if request.method == 'POST' and form.validate_on_submit():
        mase = int(request.form['svoris'])
        ugis = int(request.form['ugis'])
        funkcija = kuno_mases_indeksas(ugis, mase)
        return render_template("kuno_mases_indeksas.html", form=form, funkcija=funkcija)
    return render_template("kuno_mases_indeksas.html", form=form)


@app.route('/dienos_kaloriju_norma', methods=['GET', 'POST'])
def dkn():
    form = forms.DienosKalorijuForma()
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
    data = Straipsnis.query.filter_by(id=id)
    return render_template('straipsnis.html', pavadinimas=pavadinimas, tema=tema, id=id, data=data.all(),
                           datetime=datetime)


@app.route("/prideti_straipsni", methods=['GET', 'POST'])
@login_required
def prideti_straipsni():
    db.create_all()
    form = forms.StraipsnisForma()
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


@app.route("/mano_straipsniai")
@login_required
def mano_straipsniai():
    page = request.args.get('page', 1, type=int)
    data = Straipsnis.query.filter_by(vardas=current_user.vardas).order_by(Straipsnis.data.desc()).paginate(page=page, per_page=9)
    return render_template('mano_straipsniai.html', data=data, datetime=datetime)


@app.route("/delete/<id>")
@login_required
def istrinti_straipsni(id):
    istrinti = Straipsnis.query.get(id)
    db.session.delete(istrinti)
    db.session.commit()
    return redirect(url_for("mano_straipsniai"))


@app.route("/update/<int:id>", methods=['GET', 'POST'])
def redaguoti_straipsni(id):
    forma = forms.StraipsnisForma()
    straipsnis1 = Straipsnis.query.get(id)
    if forma.validate_on_submit():
        straipsnis1.pavadinimas = forma.pavadinimas.data
        straipsnis1.tema = forma.tema.data
        straipsnis1.tekstas = forma.tekstas.data
        db.session.add(straipsnis1)
        db.session.commit()
        flash('Sėkmingai redagavote.', 'success')
        return redirect(url_for('mano_straipsniai'))
    return render_template("redaguoti_straipsni.html", form=forma, straipsnis=straipsnis1)


@app.route("/issukis", methods=['GET', 'POST'])
@login_required
def issukis():
    form = forms.IssukisForma()
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


@app.route("/paskyra")
@login_required
def paskyra():
    vardas = current_user.vardas
    el_pastas = current_user.el_pastas
    return render_template('paskyra.html', vartotojas=vardas, pastas=el_pastas)


@app.errorhandler(404)
def klaida_404(klaida):
    return render_template("404.html"), 404


@app.errorhandler(403)
def klaida_403(klaida):
    return render_template("403.html"), 403


@app.errorhandler(500)
def klaida_500(klaida):
    return render_template("500.html"), 500


