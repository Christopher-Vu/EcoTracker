from flask import Flask, request, render_template, session
import re
import sqlite3
from frontend import app
import frontend.Backend.calculator as calc

#Establish connection/cursor, create database (leaving this code here just for ease of addition in the future)
"""
conn = sqlite3.connect('frontend/Backend/userdata.db')
c = conn.cursor()
c.execute("CREATE TABLE userdata (email TEXT,password TEXT);")
conn.commit()
conn.close()
"""

# Route user to the proper page 
@app.route('/')
def home():
    return render_template('landing.html', logged_in=session.get('logged', False))

@app.route('/landing.html')
def landing():
    return render_template('landing.html', logged_in=session.get('logged', False))

@app.route('/logged_out.html')
def log_out():
    session['logged'], session['current_user'] =False, None
    return render_template('landing.html', logged_in=False)

@app.route('/calculator.html')
def calculator_page():
    return render_template('calculator.html', logged_in=session.get('logged', False))

@app.route('/login.html')
def login_page():
    return render_template('login.html', logged_in=session.get('logged', False))

@app.route('/signup.html')
def signup_page():
    return render_template('signup.html', logged_in=session.get('logged', False))

@app.route('/logger.html')
def logger_page():
    if not session.get('logged', False): return render_template('signup.html', show_error=True, error_message="Signup to use logger")
    return render_template('logger.html')

@app.route('/sources.html')
def sources_page():
    print(f"{session.get('logged', False)}, {session.get('current_user', None)}")
    return render_template('sources.html', logged_in=session.get('logged', False))

@app.route('/stats.html')
def stats_page():
    if not session.get('logged'): return render_template('signup.html', show_error=True, error_message="Signup to see stats")
    return render_template('stats.html')

@app.route('/tasks.html')
def tasks_page():
    return render_template('tasks.html', logged_in=session.get('logged', False))

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['pass']
    password2 = request.form['confirm-pass']

    if not valid_email(email):
        return render_template('signup.html', show_error=True, error_message='Email is invalid')
    
    conn = sqlite3.connect('frontend/Backend/userdata.db')
    c = conn.cursor()

    c.execute("SELECT * FROM userdata WHERE email=?", (email,))
    row = c.fetchone()

    if password != password2: 
        return render_template('signup.html', show_error=True, error_message='Passwords do not match')

    elif row is None: #email doesn't exist yet
        c.execute(f"INSERT INTO userdata (email, password) VALUES ('{email}', '{password}');")
        conn.commit()
        conn.close()
        session['current_user'], session['logged'] = email, True
        return render_template('landing.html', logged_in=True)  

    conn.close()
    return render_template('signup.html', show_error=True, error_message='Email already exists')
        
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['pass']

    if not valid_email(email):
        return render_template('login.html', show_error=True, error_message='Email is invalid')

    conn = sqlite3.connect('frontend/Backend/userdata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM userdata WHERE email=?", (email,))
    row = c.fetchone()

    if row is None: #email doesn't exist
        conn.close()
        return render_template('login.html', show_error=True, error_message='Email does not exist')
    elif row[1] == password: # password matches
        conn.close()
        session['current_user'], session['logged'] = email, True
        print(f"{session.get('logged', False)}, {session.get('current_user', None)}")
        return render_template('landing.html', logged_in=True)  

    else: # password doesn't match (duh)
        conn.close()
        return render_template('login.html', show_error=True, error_message='Password is incorrect')

@app.route('/calculator', methods=['POST'])
def calculator():
    avg_footprint = calc.avg_footprint(request.form['people'], request.form['income'])
    goods = calc.goods(request.form['clothing'], request.form['electronics'], request.form['furniture'], request.form['other']) 
    food = calc.food(request.form['beef'], request.form['meat'], request.form['other'])
    energy = calc.energy(request.form['electricity_bill'], request.form['cpkwh'], request.form['clean_percent'])
    water = calc.water(request.form['water_bill'], request.form['cpg'])
    transport = calc.transport(request.form['Dmiles'], request.form['Dmpg'], request.form['Gmiles'], request.form['Gmpg'], request.form['flight_hours'], request.form['transit'])
    days = request.form['time']

    total_footprint = goods + food + energy + water + transport
    tpy = total_footprint / days * 365
    comparison = tpy / avg_footprint
    if comparison > 1: comparison, context = f'{round(1 - comparison, 2)}', 'worse than average'
    else: comparison, context = f'{abs(1 - round(tpy / comparison, 2))}', 'better than average'
    return render_template('calculator.html', footprint = total_footprint, tpy = tpy, comparison = comparison, comparison_context=context)


def printuserdata():
    conn = sqlite3.connect('frontend/Backend/userdata.db')
    c = conn.cursor()
    c.execute("DELETE FROM userdata")
    c.execute('SELECT * FROM userdata')
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()

def valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)
