# Imports Obviously
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, \
    login_user, logout_user, current_user, login_required



# Basic Setup shiz
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='MyKeyIsTheDankest'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)



# Routes
@app.route('/')
def home():
    return render_template('index.html')



# Table/Models
class HlthyRec(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    ingredients =   db.Column(db.String(1000))
    preperation =   db.Column(db.String(10000))
    cooking     =   db.Column(db.String(10000))
    userId      =   db.Column(db.Integer, db.ForeignKey('user.id'))

class DankRec(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    ingredients = db.Column(db.String(1000))
    preperation = db.Column(db.String(10000))
    cooking     = db.Column(db.String(1000))
    userId      = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    name     = db.Column(db.String(40), nullable=False)
    hlthyrec = db.relationship('HlthyRec', backref='user')
    dankrec  = db.relationship('DankRec', backref='user')


@login_manager.user_loader
def load_user(uid):
    user = User.query.get(uid)
    return user


if __name__=="__main__":
    app.run()
