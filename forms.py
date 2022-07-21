from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email


class PridejimoForma(FlaskForm):
    produktas = StringField('Produktas', [DataRequired()])
    kalorijos = IntegerField('Kalorijos', [DataRequired()])
    baltymai = FloatField('Baltymai', [DataRequired(message='Neteisingai įvesta!')])
    angliavandeniai = FloatField('Angliavandeniai', [DataRequired(message='Neteisingai įvesta! !')])
    riebalai = FloatField('Riebalai', [DataRequired(message='Neteisingai įvesta!')])
    prideti = SubmitField('Prideti')