from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)


app.secret_key = 'Ty?!,TheDoor4ik32143124140917498197d32j32hiw1242134'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '75398753698Bb'
app.config['MYSQL_DB'] = 'pythonlogin'


mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedIn'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('homeBreast'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedIn', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' \
            in request.form and 'password' \
            in request.form and 'email' \
            in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            mysql.connection.commit()
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)


@app.route('/homeBreast')
def homeBreast():
    if 'loggedIn' in session:
        return render_template('homeBreast.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/homeSpin')
def homeSpin():
    if 'loggedIn' in session:
        return render_template('homeSpin.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/homeLegs')
def homeLegs():
    if 'loggedIn' in session:
        return render_template('homeLegs.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if 'loggedIn' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


@app.route("/calculator", methods=['GET', 'POST'])
def calculator():
    daily_calories = 1
    if 'loggedIn' in session:
        if request.method == 'POST':
            gender = request.form['gender']
            age = float(request.form['age'])
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            activity = float(request.form['activity'])

            if gender and height and weight and activity:
                if gender == 'male':
                    daily_calories = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)

                elif gender == 'female':
                    daily_calories = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

            daily_calories *= activity
        return render_template('calculator.html', daily_calories=daily_calories)

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
