# For ease of testing
import sqlite3

def dothething():
    conn = sqlite3.connect('frontend/Backend/userdata.db')
    c = conn.cursor()
    c.execute("CREATE TABLE userdata (email TEXT,password TEXT);")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    dothething()