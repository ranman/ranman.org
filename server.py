from flask import Flask, render_template
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)


@app.route('/')
def home_page():
    return render_template('ranman.html')


if __name__ == '__main__':
    app.run()
