from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bcrypt import Bcrypt
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import os, glob
from forms import RegistrationForm, Login
import requests
from forms import SearchForm
from hackernews import *
from flask_login import LoginManager, UserMixin, login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from youtube import video_list
from youtube2 import resume_list


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ede080d803e9f6d30ce3348400e0b49b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
proxied = FlaskBehindProxy(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)

folder = os.path.join('static')
app.config['UPLOAD_FOLDER'] = folder

# create users database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Integer, unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
    
class SavedJob(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    company = db.Column(db.String(80), nullable=False)
    link = db.Column(db.String(150))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    user = db.relationship('User',
        backref=db.backref('saved_jobs', lazy=True))

    def __repr__(self):
        return '<Job %r>' % self.title

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect((url_for('login')))

@app.route("/")
def landing():
    search = request.args.get('search')
    print(search)
    if request.method == 'GET' and search:
        return redirect((url_for('results', query=search)))  # or what you want
    
    link="/login"
    if current_user.is_authenticated:
        num = current_user.get_id()
        user = User.query.filter_by(id=num).first()
        link = "/{}".format(user.username)
        return render_template('landing.html', subtitle='landing page', text='This is the home page', link=link, user=user.username)
    return render_template('landing.html', subtitle='landing page', text='This is the home page', link=link, user="Login")


@app.route("/home", methods=['GET'])
def home():
    search = request.args.get('search')
    print(search)
    if request.method == 'GET' and search:
        #print(str(form.search.data))
        return redirect((url_for('results', query=search)))  # or what you want
    return render_template('home.html', subtitle='Home page', text='This is the home page')

@app.route("/career")
def career():
    return render_template('career.html', subtitle='careers page', text='This is the careers page')

@app.route("/feed")
def feed():
    search = request.args.get('search')
    print(search)
    if request.method == 'GET' and search:
        #print(str(form.search.data))
        return redirect((url_for('results', query=search)))  # or what you want
    stories = story_list
    
    link="/login"
    if current_user.is_authenticated:
        num = current_user.get_id()
        user = User.query.filter_by(id=num).first()
        link = "/{}".format(user.username)
        return render_template('feed.html', stories=stories, link=link, user=user.username)
    return render_template('feed.html', stories=stories, link=link, user="Login")

@app.route("/interview")
def interview():
    videos = video_list
    return render_template('youtube.html', videos=videos)

@app.route("/resume")
def resume():
    videos = resume_list
    return render_template('youtube2.html', videos=videos)

@app.route("/about")
def about():
    search = request.args.get('search')
    print(search)
    if request.method == 'GET' and search:
        #print(str(form.search.data))
        return redirect((url_for('results', query=search)))  # or what you want
    return render_template('about.html', subtitle='about page', text='This is the about page')

# registration
@app.route("/register", methods=['GET', 'POST'])
def register():
    search = request.args.get('search')
    print(search)
    if request.method == 'GET' and search:
        return redirect((url_for('results', query=search)))
    
    form = RegistrationForm()
    if form.validate_on_submit(): # checks if entries are valid
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# log in if already has an user
@app.route("/login", methods=['GET', 'POST'])
def login():
    search = request.args.get('search')
    if request.method == 'GET' and search:
        return redirect((url_for('results', query=search)))
    
    
    form = Login()
    user_name = form.username.data
    password = form.password.data
    if form.validate_on_submit():
        user = User.query.filter_by(username=user_name).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('user', name = form.username.data))
        flash('Invalid username or password.')
        

    return render_template('login.html', title='Login', form=form)


@app.route('/<name>')
@login_required
def user(name):
    link="/login"
    if current_user.is_authenticated:
        num = current_user.get_id()
        user = User.query.filter_by(id=num).first()
        link = "/{}".format(user.username)
    search = request.args.get('search')
    if request.method == 'GET' and search:
        return redirect((url_for('results', query=search)))
    def images():
        tracker = []
        y = []
        if os.path.exists('JobHub/static/'+name):
            for filename in os.listdir("JobHub/static/"+name):
                if name in str(filename):
                    tracker.append(str(filename))
            for x in tracker:
                graph = os.path.join(app.config['UPLOAD_FOLDER'], '/static/'+name+'/'+x)
                y.append(graph)
            return y
    image = images()
    
    num = current_user.get_id()
    user = User.query.filter_by(id=num).first()
    jobs = user.saved_jobs
    size = len(jobs)
    
    if not image:
        return render_template('user_page.html', subtitle='Hello, ' + name + '!', link=link, user=user.username, jobs=jobs, size=size)
    else:
        return render_template('user_page.html', subtitle='Hello, ' + name + '!', names=image, link=link, user=user.username, jobs=jobs, size=size)


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    print(form.validate_on_submit())
    if request.method == 'POST':
        return redirect((url_for('results', query=form.search.data)))  # or what you want
    return render_template('search.html', form=form)


def parse_job(job):
    data = job.split(',')
    return data[0], data[1], data[2]


@app.route("/results/<query>")
def results(query):
    search = request.args.get('search')
    job = request.args.get('save')
    user_name = request.args.get('user_name')
    print(job)
#     print(save)
    if request.method == 'GET' and job:
        job_title, job_link, company = parse_job(job)
        num = current_user.get_id()
        user = User.query.filter_by(id=num).first()
        job = SavedJob(title=job_title, link=job_link, company=company, user=user)
        db.session.add(job)
        db.session.commit()

    if request.method == 'GET' and search:
        return redirect((url_for('results', query=search)))  # or what you want
        
    """
    SAMPLE RESPONSE
    {
        'title': 'IT Software Developer', 
        'location': 'Burke, VA', 
        'snippet': '&nbsp;...Job Summary \r\n ASSIGNMENT DESCRIPTION: 
            <b>Software </b>Developers identify, document, and analyze customer, business, and system 
            requirements; evaluate alternative approaches; and design and develop solutions tailored 
            to specific agency, systems, and customer requirements....&nbsp;', 
        'salary': '', 
        'source': 'jobs2careers.com', 
        'type': '', 
        'link': 'https://jooble.org/desc/-9059355599196008744?ckey=it%2c+software&rgn=0&pos=1&elckey=-8038956014579985282&p=1&aq=8188911676283653946&age=39&relb=175&brelb=115&bscr=6036.0728&scr=9185.328173913043', 
        'company': 'National Geospatial-Intelligence Agency (NGA)', 
        'updated': '2021-07-29T10:11:51.6948763+03:00', 
        'id': -9059355599196008744
    }
    """
    # get content from search bar
    API_KEY = "0ce30d04-327c-401b-8ead-9276e407a7b1" # jooble
    BASE_URL = "https://jooble.org/api/"
    #request headers
    headers = {"Content-type": "application/json"}
    # from search bar
    keywords = query
    body = '{ "keywords": "' + '{}'.format(query) + '", "location": "United States"}'
    response = requests.post(BASE_URL + API_KEY, data=body, headers=headers)
    data = response.json()
    # total num of jobs
    num_jobs = data['totalCount']
    # list of jobs
    jobs = data['jobs']
    
    link="/login"
    if current_user.is_authenticated:
        num = current_user.get_id()
        user = User.query.filter_by(id=num).first()
        link = "/{}".format(user.username)
        return render_template("results.html", jobs=jobs, link=link, user=user.username)
    return render_template("results.html", jobs=jobs, link=link, user="Login")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")