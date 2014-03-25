from flask import Flask, render_template
from flask.ext.pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config.update({'MONGO_DBNAME': 'randall'})
app.debug = True
mongo = PyMongo(app)


@app.route('/')
def home_page():
    events = list(mongo.db.events.find().sort("date", -1))
    for index in range(len(events)):
        if events[index].get('date').replace(tzinfo=None) <= datetime.now():
            break
    upcoming = events[:index]
    past = events[index:]
    return render_template('ranman.html', upcoming=upcoming, past=past)


if __name__ == '__main__':
    app.run()
