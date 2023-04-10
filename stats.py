import sqlite3
from flask import render_template_string

def generate_stats(email):
    stat_string = ""

    conn = sqlite3.connect('frontend/Backend/userdata.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM {email}")
    results = cursor.fetchall()

    for row in results:
        stat_string = stat_string + f'→ {row[0]} (Data was taken over a {row[1]} day period):\nTotal Carbon Footprint: {row[2]} Tons.\nTheorertical Yearly Foorprint: {row[3]} Tons.\nThis Theoretical Footprint is {row[4]} {row[5]}.\n\n'

    cursor.close()
    conn.close()

    return render_template_string(stat_string)