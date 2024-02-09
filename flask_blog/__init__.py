from flask import Flask 
import os 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)#crée une instance de l'application Flask

app.config['SECRET_KEY'] = '713331dfeaff23876f4cea80bdfe7df3'#configure une clé secrète utilisée pour sécuriser les sessions et les cookies
#pour genere cette cle secrete
# python
#import secrets
#secrets.token_hex(16)
#exit()

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)


from flask_blog import routes
with app.app_context():
     db.create_all()