from urllib.request import urlcleanup
from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3

app = Flask(__name__)
app.secret_key="95321910"

def init_db():
    db = sqlite3.connect('users.db')
    with open('schema.sql', 'r') as schema:
        db.executescript(schema.read())
    db.commit()

@app.cli.command('initdb')
def initdb_cmd():
    init_db()
    print("Initialised database.")

def get_db():
    con = sqlite3.connect('users.db')
    con.row_factory = sqlite3.Row
    return con

@app.route('/')
def index():
    return render_template('index.html', title='Home')


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/signin', methods=('GET', 'POST'))
def signin():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT password FROM users WHERE username = ?', (username, )
        ).fetchone()
        
        if user is None:
            error = 'Incorrect Username/Password.'
        elif password != user['password']:
            print(user)
            error = 'Incorrect Password.'

        if error is None:
            return redirect(url_for('index'))
        flash(error)
        db.close()

    return render_template('signin.html', title='Sign In', error=error)


@app.route('/signup', methods=('POST', 'GET'))
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        name = request.form['name']
        db = get_db()
        cur = db.cursor()
        
        cur.execute(
            'INSERT INTO users (username, password, email, name) VALUES (?, ?, ?, ?);', (username, password, email, name)
        )
        db.commit()
        cur.close()
        db.close()
        return render_template('index.html', title="Home", success="Registration Successfull!")
        

    return render_template('signup.html', title='Sign Up')
       
      
@app.route('/user',methods=["GET","POST"])
def user():
    return render_template("user.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)