from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, \
    login_user, logout_user, current_user, login_required


app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='MyKeyIsTheDankest'
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('index.html')

class HealthyRecipe(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    ingredients =   db.Column(db.String(1000))
    preperation =   db.Column(db.String(10000))
    cooking     =   db.Column(db.String(10000))

class DankRecipe(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    ingredients = db.Column(db.String(1000))
    preperation = db.Column(db.String(10000))
    cooking     = db.Column(db.String(1000))

class User(UserMixin, db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    name     = db.Column(db.String(40), nullable=False)


if __name__=="__main__":
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    app.run()
