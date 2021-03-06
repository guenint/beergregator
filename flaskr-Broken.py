from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
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

#def get_users_from_file(filename):
#    user_names = {}
#    with open(filename, 'r') as f:
#        for line in f:
#            print line
#            i = 1
#            values = line.rsplit(',')
#           print values
#           if len(values) > 2:
#               u = User(values[1], values[2], int(values[0]))
#                USERS[i]=(u)
#                user_names[u.name] = u;
#            i +=1
#        f.close()
#        print user_names
#   return user_names

USERS = {
    1: User(u"Noth", u"pass", 1),
    2: User(u"Steve", u"pass", 2),
    3: User(u"Creeper",u"pass", 3, False),
}


USER_NAMES = dict((u.name, u) for u in USERS.itervalues())

#users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]


#USER_NAMES = get_users_from_file("users.txt")


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
def load_user(userid):
    return USERS.get(int(id))

login_manager.setup_app(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    print "hello db"
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()
    print "db closed"

def get_users_from_db():
    cur = g.db.execute('select username, password from users order by id desc')
    print "hello3"
    USERS = []
    USER_NAMES = {}
    for row in cur.fetchall():
        print row
        USER_NAMES.append(User(row[1], row[2], row[0]))
    for user in USERS:
        USER_NAMES[user.name] = user
    return USER_NAMES

#USER_NAMES = get_users_from_db()
#

@app.route('/show_beers')
def show_beers():
    print "try"
    d = aggregate_types(["lV8gC4","3A5MHE","WXBFIy","lV8gC4","lAcrbq","iBzEfC"])
    print d

@app.route('/')
def show_users():
    print "hello"
    cur = g.db.execute('select username, password from users order by id desc')
    print "hello3"
    users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
    print users
    print "hello2"
    return render_template('show_users.html', users=users)

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
        print("got username from form")   
        if username in USER_NAMES:
            print("getting user name from USER_NAMES")
            remember = request.form.get("remember", "no") == "yes"
            print("requested remember me form")
            if login_user(USER_NAMES[username], remember=remember):
                print("logging in user")
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")


"""
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        if username in USER_NAMES:
            remember = request.form.get("remember", "no") == "yes"
            if login_user(USER_NAMES[username], remember=remember):
                flash("Logged in!")
                return redirect(request.args.get("next") or url_for("index"))
            else:
                flash("Sorry, but you could not log in.")
        else:
            flash(u"Invalid username.")
    return render_template("login.html")
"""

""" 
        
        cur = g.db.execute('select username, password from users order by id desc')        
        users = [(username = row[1], password = row[1]) for row in cur.fetchall()]
        for user in users:
            database_user, database_pass = user
            if username == database_user:
                remember = request.form.get("remember", "no") == "yes"
                if login_user(database_pass, remember = remember):
                    flash("Logged in!")
                    return redirect(request.args.get("next") or url_for("index"))
                else:
                    flash("Sorry, but you could not log in.")
            else:
                flash(u"Invalid username.")
        return render_template("login.html")
"""
"""    

    if form.validate_on_submit():
        login_user(user)
        flash("Logged in Successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    else:
        flash("failed to log in")
    return render_template("login.html", form = form)
"""
"""
    error = None
    if request.method == "POST" and "username" in request.form:
        username = request.form["username"]
        password = request.form["password"]
        print username
        print password
        cur = g.db.execute('select username, password from users order by id desc')
        users = [dict(username=row[0], password=row[1]) for row in cur.fetchall()]
        print users
        print len(users)
        for user in users:
            print user['username']
            print user['password']
            if user['username'] == username  and user['password'] == password:
                remember = request.form.get("remember", "no") == "yes"
                if login_user(username, remember = remember):
                    print("log in occurs")
                    flash("Logged in!")
                    return redirect(request.args.get("next") or url_for("show_users"))    
            else:
                print("pass failed")
                flash("Sorry, but you could not log in.")
                error = "Invalid pass."
        else:
            flash(u"Invalid username.")
            error = "Invalid username."
            print("invalid username")
    return render_template("login.html", error=error)
"""

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('show_beers'))

@app.before_request
def before_request():
    print "before_request"
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    print "after_request"
    g.db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0')

