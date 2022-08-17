from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, FloatField, IntegerField, SelectField, \
    TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from svetaine.models import Vartotojas


class PridejimoForma(FlaskForm):
    produktas = StringField('Produktas', [DataRequired()])
    kalorijos = IntegerField('Kalorijos (kcal)', [DataRequired()])
    baltymai = FloatField('Baltymai', [DataRequired(message='Neteisingai įvesta!')])
    angliavandeniai = FloatField('Angliavandeniai', [DataRequired(message='Neteisingai įvesta! !')])
    riebalai = FloatField('Riebalai', [DataRequired(message='Neteisingai įvesta!')])
    prideti = SubmitField('Prideti')


class TikrintiForma(FlaskForm):
    ieskoti = StringField('Produktas', [DataRequired()])
    svoris = IntegerField('Svoris (gramais)', [DataRequired()])
    tikrinti = SubmitField('Tikrinti')


class KalorijuForma(FlaskForm):
    ugis = IntegerField("Ūgis (cm)", [DataRequired()])
    svoris = IntegerField("Svoris (kg)", [DataRequired()])
    skaiciuoti = SubmitField('Skaičiuoti')


class DienosKalorijuForma(FlaskForm):
    ugis = IntegerField("Ūgis (cm)", [DataRequired()])
    svoris = IntegerField("Svoris (kg)", [DataRequired()])
    amzius = IntegerField("Amžius (metais)", [DataRequired()])
    lytis = SelectField('Lytis', choices=[('Vyras', 'Vyras'), ('Moteris', 'Moteris')])
    intensyvumas = SelectField('Fizinis aktyvumas per savaitę', choices=[
        ('Pasyvus 0-1val.', 'Pasyvus 0-1val.'),
        ('Lengvai aktyvus 1-2val.', 'Lengvai aktyvus 1-2val.'),
        ('Vidutiniškai aktyvus 2-3val', 'Vidutiniškai aktyvus 2-3val'),
        ('Labai aktyvus 3-4val.', 'Labai aktyvus 3-4val.'),
        ('Ypač aktyvus 5+ val.', 'Ypač aktyvus 5+ val.')])
    skaiciuoti = SubmitField('Skaičiuoti')


class RegistracijosForma(FlaskForm):
    vardas = StringField('Vardas', [DataRequired()])
    el_pastas = StringField('El. paštas', [DataRequired()])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    patvirtintas_slaptazodis = PasswordField("Pakartokite slaptažodį",
                                             [EqualTo('slaptazodis', "Slaptažodis turi sutapti.")])
    submit = SubmitField('Prisiregistruoti')

    def tikrinti_varda(self, vardas):
        vartotojas = Vartotojas.query.filter_by(vardas=vardas.data).first()
        if vartotojas:
            raise ValidationError('Šis vardas panaudotas. Pasirinkite kitą.')

    def tikrinti_pasta(self, el_pastas):
        vartotojas = Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if vartotojas:
            raise ValidationError('Šis el. pašto adresas panaudotas. Pasirinkite kitą.')


class PrisijungimoForma(FlaskForm):
    el_pastas = StringField('El. paštas', [DataRequired()])
    slaptazodis = PasswordField('Slaptažodis', [DataRequired()])
    prisiminti = BooleanField("Prisiminti mane")
    submit = SubmitField('Prisijungti')


class UzklausosAtnaujinimoForma(FlaskForm):
    el_pastas = StringField('El. paštas', validators=[DataRequired(), Email()])
    submit = SubmitField('Gauti')

    def validate_email(self, el_pastas):
        user = Vartotojas.query.filter_by(el_pastas=el_pastas.data).first()
        if user is None:
            raise ValidationError('Nėra paskyros, registruotos šiuo el. pašto adresu. Registruokitės.')


class SlaptazodzioAtnaujinimoForma(FlaskForm):
    slaptazodis = PasswordField('Slaptažodis', validators=[DataRequired()])
    patvirtintas_slaptazodis = PasswordField('Pakartokite slaptažodį', validators=[DataRequired(), EqualTo('slaptazodis')])
    submit = SubmitField('Atnaujinti Slaptažodį')


class StraipsnisForma(FlaskForm):
    pavadinimas = StringField('Pavadinimas', [DataRequired()])
    tema = SelectField('Tema', choices=[
        ('Mityba', 'Mityba'),
        ('Sportas', 'Sportas'),
        ('Sveikata', 'Sveikata')])
    tekstas = TextAreaField('Tekstas', render_kw={"rows": 10, "cols": 10})
    submit = SubmitField('Ikelti')


class IssukisForma(FlaskForm):
    pasirinkimas = SelectField('Pasirinkti', choices=[
        ('Lengvas', 'Lengvas'),
        ('Vidutinis', 'Vidutinis'),
        ('Sunkus', 'Sunkus')])
    submit = SubmitField('Atsisiųsti')