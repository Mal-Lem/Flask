from flask_blog import db, app , login_manager
from datetime import datetime
from flask_login import UserMixin
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import Serializer as Serializer

@login_manager.user_loader
def load_user(user_id):
   return User.query.get(int(user_id))

class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20),unique=True,nullable=False)
   email = db.Column(db.String(120),unique=True,nullable=False)
   image_file = db.Column(db.String(20),nullable=False, default='./img.png')
   password = db.Column(db.String(60),nullable=False)
   posts = db.relationship('Post',backref='author',lazy=True)

   def get_reset_token(self, expires_sec=1800):
       s = Serializer(app.config['SECRET_KEY'], expires_sec)
       return s.dumps({'user_id': self.id}).decode('utf-8')
   
   @staticmethod
   def verify_reset_token(token):
       s = Serializer(app.config['SECRET_KEY'])
       try :
           user_id = s.loads(token)['user_id']
       except :
           return None  
       return User.query.get(user_id) 
    
   def __repr__(self):
      return f"User('{self.username}', '{self.email}','{self.image_file}')"

class Post(db.Model):
      id = db.Column(db.Integer, primary_key=True)
      title = db.Column(db.String(100),nullable=False)
      date_posted = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
      content = db.Column(db.Text, nullable=False)
      user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
      def __repr__(self):
         return f"Post('{self.title}', '{self.date_posted}')"
with app.app_context():
      db.create_all()

    # si vous voulez verifier votre base de donnees 
    #from flask_blog import db, app
    #app.app_context().push()
    #from flask_blog.model import User, Post
    #db.create_all()
    #User.query.all()
    #user = User.query.first()

    #https://stackoverflow.com/questions/73961938/flask-sqlalchemy-db-create-all-raises-runtimeerror-working-outside-of-applicat


#     pour importer quoi que ce soit 
# from flask_blog import app
# >>> app.app_context().push()
# >>> from flask_blog.model import Post
# >>> posts = Post.query.all()
#  for post in posts:
# ...    print(post)