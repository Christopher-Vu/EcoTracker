from flask import Flask, request, render_template, session
import re
import sqlite3
import base64
from frontend import app
import frontend.Backend.calculator as calc
from frontend.Backend.stats import generate_stats, problem_area
from frontend.Backend.tasks import tasks
from frontend.Backend.graphs import footprint_pie

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
    return render_template('calculator.html', submitted=False, logged_in=session.get('logged', False))

@app.route('/login.html')
def login_page():
    return render_template('login.html', logged_in=session.get('logged', False))

@app.route('/signup.html')
def signup_page():
    return render_template('signup.html', logged_in=session.get('logged', False))

@app.route('/logger.html')
def logger_page():
    if not session.get('logged', False): return render_template('signup.html', show_error=True, error_message="Signup to use logger")
    return render_template('logger.html', logged_in=session.get('logged', False))

@app.route('/sources.html')
def sources_page():
    print(f"{session.get('logged', False)}, {session.get('current_user', None)}")
    return render_template('sources.html', logged_in=session.get('logged', False))

@app.route('/stats.html')
def stats_page():
    if not session.get('logged'): return render_template('signup.html', show_error=True, error_message="Signup to see stats")
    stat_string = generate_stats(session.get('current_user'))
    is_data = False
    if stat_string!="": is_data=True
    return render_template('stats.html', stat_string = stat_string, is_data=is_data, logged_in=session.get('logged', False))

@app.route('/tasks.html')
def tasks_page():
    t1, t2, t3, t4, t5, t6, t7 = tasks()
    return render_template('tasks.html', t1=t1, t2=t2, t3=t3, t4=t4, t5=t5, t6=t6, t7=t7, logged_in=session.get('logged', False))

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
        session['current_user'], session['logged'] = replace_email_chars(email), True

        c.execute(f"CREATE TABLE {replace_email_chars(email)} (date TEXT, period TEXT, footprint TEXT, tpy TEXT, comparison TEXT, comparison_context TEXT, avg_footprint TEXT, goods TEXT, food TEXT, energy TEXT, water TEXT, transport TEXT);")
        conn.commit()
        conn.close()
        
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
        session['current_user'], session['logged'] = replace_email_chars(email), True
        return render_template('landing.html', logged_in=True)  

    else: # password doesn't match (duh)
        conn.close()
        return render_template('login.html', show_error=True, error_message='Password is incorrect')

@app.route('/calculator', methods=['POST'])
def calculator():
    avg_footprint, goods, food, energy, water, transport, days, total_footprint, tpy, comparison, context = calculate()
    pie_chart = footprint_pie(goods, food, energy, water, transport)
    pie_chart = base64.b64encode(pie_chart).decode('utf-8')
    area, solution = problem_area(goods, food, energy, water, transport)

    return render_template('calculator.html', submitted = True, footprint = total_footprint, tpy = tpy, comparison = comparison, comparison_context=context, logged_in=session.get('logged', False), pie_chart=pie_chart, area=area, solution=solution)


@app.route('/logger', methods=['POST'])
def logger():
    avg_footprint, goods, food, energy, water, transport, days, total_footprint, tpy, comparison, context = calculate()

    conn = sqlite3.connect('frontend/Backend/userdata.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {session['current_user']} (date, period, footprint, tpy, comparison, comparison_context) VALUES ('{request.form['date']}', '{days}', '{total_footprint}', '{tpy}', '{comparison}', '{context}', '{avg_footprint}', '{goods}', '{food}', '{energy}', '{water}', '{transport}');")
    conn.commit()
    conn.close()

    return render_template('logger.html', logged_in=session.get('logged', False))

@app.route('/message', methods=['POST'])
def message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    with open("frontend/feedback.txt", "w") as file:
        file.write(f"Name: {name}. Email: {email}. Message: {message}")
    
    return render_template('landing.html', logged_in=session.get('logged', False))

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
    
def replace_email_chars(email):
    return email.replace('@', '_').replace('.', '_')

def calculate():
    avg_footprint = calc.avg_footprint(int(request.form['people']), float(request.form['income']))
    goods = calc.goods(float(request.form['clothing']), float(request.form['electronics']), float(request.form['furniture']), float(request.form['other']))
    food = calc.food(float(request.form['beef']), float(request.form['meat']), float(request.form['other']))
    energy = calc.energy(float(request.form['electricity_bill']), float(request.form['cpkwh']), float(request.form['clean_percent']))
    water = calc.water(float(request.form['water_bill']), float(request.form['cpg']))
    transport = calc.transport(float(request.form['Dmiles']), float(request.form['Dmpg']), float(request.form['Gmiles']), float(request.form['Gmpg']), float(request.form['flight_hours']), float(request.form['transit']))
    days = float(request.form['time'])

    total_footprint = round(goods + food + energy + water + transport, 2)
    tpy = round(total_footprint / days * 365, 2)
    comparison = tpy / avg_footprint

    if comparison > 1: comparison, context = f'{round(abs(comparison - 1) * 100, 2)}%', 'worse than average'
    else: comparison, context = f'{round(abs(1 - comparison) * 100, 2)}%', 'better than average'
    
    return avg_footprint, goods, food, energy, water, transport, days, total_footprint, tpy, comparison, context