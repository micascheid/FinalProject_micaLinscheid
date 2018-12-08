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
    return render_template('home.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user.username == username and user.password==password:
            login_user(user)
            return redirect('/profile')
        else:
            print("So you can't remember your credential? That sucks! HAHA")
    return render_template('/login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method=='POST':
        username = request.form['usernameS']
        password = request.form['passwordS']
        name = request.form['nameS']

        # User object
        user = User(username=username, password=password, name=name)

        # Commit new user
        db.session.add(user)
        db.session.commit()

    return redirect('/')

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def usershit():
    if request.method=='POST':
        if request.form['recType']=='Healthy Recipe':
            name = request.form['recname']
            ingredients = request.form['ingredients']
            preperation = request.form['preperation']
            cooking = request.form['cooking']

            # Create hlthyrec object
            hlthyrec = HlthyRec(name=name, ingredients=ingredients, preperation=preperation, cooking=cooking)
            # Set owner of this recipe
            hlthyrec.userId = current_user.id
            db.session.add(hlthyrec)
            db.session.commit()

        if request.form['recType']=='That Dank Dank':
            name = request.form['recname']
            ingredients = request.form['ingredients']
            preperation = request.form['preperation']
            cooking = request.form['cooking']

            dankrec = DankRec(name=name, ingredients=ingredients, preperation=preperation, cooking=cooking)
            dankrec.userId=current_user.id

            db.session.add(dankrec)
            db.session.commit()

    return render_template('/profile.html')

    # TODO else if recType isn't entered


# Table/Models
class HlthyRec(db.Model):
    id =            db.Column(db.Integer, primary_key=True)
    name        =   db.Column(db.String(100))
    ingredients =   db.Column(db.String(1000))
    preperation =   db.Column(db.String(10000))
    cooking     =   db.Column(db.String(10000))
    userId      =   db.Column(db.Integer, db.ForeignKey('user.id'))

class DankRec(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100))
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


if __name__ == "__main__":
    app.run()
