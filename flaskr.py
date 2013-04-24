from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from flask.ext.login import (LoginManager, current_user, login_required, login_user, logout_user, UserMixin, AnonymousUser, confirm_login, fresh_login_required)
import apiparse

class User(UserMixin):
    def __init__(self, name, password, id, active=True):
        self.name = name
        self.id = id
        self.password = password
        self.active = active

    def is_active(self):
        return self.active

class Anonymous(AnonymousUser):
    name = u"Anonymous"

class Beer_Category():
    def __init__(self, name, types):
        self.name = name
        self.types = types

USERS = {
    1: User(u"Dhruv", u"pass", 1),
    2: User(u"Teddy", u"pass", 2),
    3: User(u"Creeper",u"pass", 3, False),
}

USER_NAMES = dict((u.name, u) for u in USERS.itervalues())

#configuration
DATABASE = '/tmp/users.db'
DEBUG = False
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = u"Please log in to access this page."
login_manager.refresh_view = "reauth"

@login_manager.user_loader
def load_user(id):
    return USERS.get(int(id))

login_manager.setup_app(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/', methods = ['GET', 'POST'])
def show_users():
    return render_template('index.html')

@app.route('/show_beers', methods=['GET', 'POST'])
@login_required
def show_beers():
    location = request.form['lat'], request.form['lon']
    if location == (None,None):
        beers = apiparse.get_brews(40, 40, 100)
    else:
        beers = apiparse.get_brews(location[0], location[1], 100)
    to_display = []
    for beer in beers:
        category, specific = beer
        to_display.append(Beer_Category(category, specific))
    return render_template('beer.html', to_display=to_display[0:5], location=location)

@app.route('/adduser', methods=['POST'])
def add_user():
    g.db.execute('insert into users (username, password) values (?, ?)',
            [request.form['username'], request.form['password']])
    g.db.commit()
    flash('New user created')
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        print username
        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            print "remember"
            if login_user(USER_NAMES[username], remember=remember):
                print "Logged in"
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("show_users"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_users'))

"""@app.before_request
def before_request():
    print "before_request"
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    print "after_request"
    g.db.close()
"""
if __name__ == '__main__':
    app.run(host='0.0.0.0')

