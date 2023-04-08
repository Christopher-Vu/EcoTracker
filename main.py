from flask import Flask, request, jsonify, render_template
import sqlite3
from frontend import app

if __name__ == '__main__':
    app.run(debug=True)