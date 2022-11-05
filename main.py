from flask import Flask
from flask import url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"