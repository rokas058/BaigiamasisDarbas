import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user
from flask_mail import Mail
from os import environ

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'rųafsgasghagaa025p'.encode('utf-8')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'sportas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()

from svetaine.models import Vartotojas, Straipsnis, Maistingumas
from svetaine.models import *

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'registruotis'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(vartotojo_id):
    db.create_all()
    return Vartotojas.query.get(int(vartotojo_id))


class ManoModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.el_pastas == "rokas.prabusas@gmail.com"


admin = Admin(app)
admin.add_view(ManoModelView(Vartotojas, db.session))
admin.add_view(ManoModelView(Straipsnis, db.session))
admin.add_view(ManoModelView(Maistingumas, db.session))

psw = environ.get('slaptazodis')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'rokas.prabusas058@gmail.com'
app.config['MAIL_PASSWORD'] = psw
mail = Mail(app)


from svetaine import routes




