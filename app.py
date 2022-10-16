from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, IT\'s an API what to do querys to ThingWeb'
if __name__ == "__main__":
    app.run(debug=True)