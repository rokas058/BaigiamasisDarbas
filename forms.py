from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length


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
