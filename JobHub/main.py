from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import os, glob
from forms import RegistrationForm, Login

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ede080d803e9f6d30ce3348400e0b49b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
proxied = FlaskBehindProxy(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

folder = os.path.join('static')
app.config['UPLOAD_FOLDER'] = folder

# create users database
class User(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), unique=True, nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   password = db.Column(db.String(60), nullable=False)

   def __repr__(self):
      return f"User('{self.username}', '{self.email}')"
      
@app.route("/")

@app.route("/home")
def home():
   return render_template('home.html', subtitle='Home page', text='This is the home page')

@app.route("/career")
def career():
   return render_template('career.html', subtitle='careers page', text='This is the careers page')

@app.route("/about")
def about():
   return render_template('about.html', subtitle='about page', text='This is the about page')

# registration
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        bcrypt.check_password_hash(pw_hash, form.password.data) # returns True
        user = User(username=form.username.data, email=form.email.data, password=pw_hash)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user', name = form.username.data)) # if so - send to specific page
    return render_template('register.html', title='Register', form=form)


# log in if already has an user
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit(): # checks if entries are valid
        pw_hash = bcrypt.generate_password_hash(form.password.data)
        bcrypt.check_password_hash(pw_hash, form.password.data) # returns True
        return redirect(url_for('user', name = form.username.data)) # if so - send to specific page
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
   app.run(debug=True, host="0.0.0.0")