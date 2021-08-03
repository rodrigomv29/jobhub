from flask import Flask, render_template, redirect, url_for, request
from flask_bcrypt import Bcrypt
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
import os, glob
from forms import RegistrationForm, Login
import requests
from forms import SearchForm
from hackernews import *


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

db.create_all()

@app.route("/")
def landing():
    search = request.args.get('search')
    print(search)
    if request.method == 'GET' and search:
        #print(str(form.search.data))
        return redirect((url_for('results', query=search)))  # or what you want
    return render_template('landing.html', subtitle='landing page', text='This is the home page')

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
    stories = story_list
    return render_template('feed.html', stories=stories)

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

@app.route('/<name>')
def user(name):
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
    if not image:
        return render_template('user_page.html', subtitle='Hello, ' + name + '!')
    else:
#         for c in image:
#             return render_template('user_page.html', subtitle='Hello, ' + name + '!', names = c)
        return render_template('user_page.html', subtitle='Hello, ' + name + '!', names = image)


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    print(form.validate_on_submit())
    if request.method == 'POST':
        #print(str(form.search.data))
        return redirect((url_for('results', query=form.search.data)))  # or what you want
    #print(str(form.search.data))
    return render_template('search.html', form=form)

@app.route("/results/<query>")
def results(query):
    print(query)
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
    
#     return jobs
    return render_template("results.html", jobs=jobs)
#     for job in jobs:
#         title = job['title']
#         location = job['location']
#         snippet = job['snippet']
#         salary = job['salary']
#         source = job['source']
#         job_type = job['type']
#         link = job['link']
#         company = job['company']
#         job = job['updated']
#         job_id = job['id']

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")