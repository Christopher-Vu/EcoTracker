from flask import Flask

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'control variable' #     ;)

from frontend.Backend.routing import *
