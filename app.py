# Imports Obviously
from flask import Flask, render_template, request, redirect, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, \
    login_user, logout_user, current_user, login_required

# Basic Setup for SQLAlchemy
app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='MyKeyIsTheDankest'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.init_app(app)


# Routes
@app.route('/')
def home():
    hlthyRecs = HlthyRec.query.filter_by(userId=1)
    dankRecs = DankRec.query.filter_by(userId=1)
    return render_template('home.html', hlthyRecs=hlthyRecs, dankRecs=dankRecs,
                           username="Staff")

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user == None:
            sorry = True
            return render_template('login.html', sorry=sorry)
        elif user.username == username  and user.password == password:
            login_user(user)
            return redirect('/profile')
    return render_template('login.html')

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
        login_user(user)
        return redirect('/profile')

@app.route('/profile', methods=['POST', 'GET'])
@login_required
def usersdata():
    id = current_user.id
    hlthyRecs = HlthyRec.query.filter_by(userId=id)
    dankRecs = DankRec.query.filter_by(userId=id)
    username = current_user.username

    if request.method=='POST':
        if request.form['recType']=='Healthy Recipe':
            recTypeCreate(HlthyRec)

        if request.form['recType']=='That Dank Dank':
            recTypeCreate(DankRec)

    return render_template('profile.html', hlthyRecs=hlthyRecs, dankRecs=dankRecs,
                           username=username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/edithlthy/<recId>', methods=['POST', 'GET'])
def edithlthy(recId):
    if request.method == 'POST':

        recType = request.form['recType']

        if recType == "Healthy Recipe":

            return recEdit(HlthyRec, recId)

        if recType == "That Dank Dank":
            recTypeCreate(DankRec)
            return recDelete(HlthyRec, recId)
    else:
        return renderRec(HlthyRec, recId, 'edithlthy.html')

@app.route('/editdank/<recId>', methods=['POST', 'GET'])
def editdank(recId):
    if request.method == 'POST':

        recType = request.form['recType']

        if recType == "That Dank Dank":
            return recEdit(DankRec, recId)

        if recType == "Healthy Recipe":
            recTypeCreate(HlthyRec)
            return recDelete(DankRec, recId)
    else:
        return renderRec(DankRec, recId, 'editdank.html')

@app.route('/hlthydelete/<recId>', methods=['GET'])
def hlthydelete(recId):
    return recDelete(HlthyRec, recId)

@app.route('/dankdelete/<recId>', methods=['GET'])
def dankdelete(recId):
    return recDelete(DankRec, recId)

@app.errorhandler(404)
def err(err):
    return render_template('404.html', err=err)


# functions
def recTypeCreate(model):
    name = request.form['recname']
    ingredients = request.form['ingredients']
    preperation = request.form['preperation']
    cooking = request.form['cooking']

    # Create object
    rectype = model(name=name, ingredients=ingredients, preperation=preperation, cooking=cooking)

    # Set owner of this recipe
    rectype.userId = current_user.id
    db.session.add(rectype)
    db.session.commit()

def recEdit(model, recId):
    rec = model.query.get(recId)

    name = request.form['recname']
    ingredients = request.form['ingredients']
    preperation = request.form['preperation']
    cooking = request.form['cooking']

    rec.name = name
    rec.ingredients = ingredients
    rec.preperation = preperation
    rec.cooking = cooking

    db.session.commit()
    return redirect('/profile')

def recDelete(model, recId):
    rec = model.query.get(recId)
    db.session.delete(rec)
    db.session.commit()
    return redirect('/profile')

def renderRec(model, recId, html):
    rec = model.query.get(recId)

    name = rec.name
    ingredients = rec.ingredients
    preperation = rec.preperation
    cooking = rec.cooking
    return render_template(html, name=name, ingredients=ingredients,
                           preperation=preperation, cooking=cooking, recId=recId)


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
