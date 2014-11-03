from flask import Flask, render_template, redirect, url_for, session
from flask_oauth import OAuth
import os
import json
import requests
import facebook
from boto.sts import STSConnection
from flask.ext.pymongo import PyMongo
from pymongo.read_preferences import ReadPreference
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET")
app.config.update({
    'MONGO_DBNAME': 'randall',
    'MONGO_HOST': os.getenv("MONGO_HOST"),
    'MONGO_READ_PREFERENCE': ReadPreference.SECONDARY_PREFERRED,
    'MONGO_REPLICA_SET': 'ranman',
})
mongo = PyMongo(app)
db = mongo.db
FACEBOOK_APP_ID = os.getenv('FACEBOOK_APP_ID', '776036972455787')
FACEBOOK_APP_SECRET = os.getenv('FACEBOOK_APP_SECRET')
oauth = OAuth()
facebook_oauth = oauth.remote_app(
    'facebook',
    base_url='https://graph.facebook.com/',
    request_token_url=None,
    access_token_url='/oauth/access_token',
    authorize_url='https://www.facebook.com/dialog/oauth',
    consumer_key=FACEBOOK_APP_ID,
    consumer_secret=FACEBOOK_APP_SECRET,
    request_token_params={'scope': ['email', 'user_groups']}
)
application = app  # do this to make beanstalk happy
application.debug = os.getenv("FLASK_DEBUG", False)


@app.route('/login')
def login():
    return facebook_oauth.authorize(
        callback=url_for('oauth_authorized', _external=True))


@facebook_oauth.tokengetter
def get_facebook_token(token=None):
    return session.get('facebook_token')


@app.route('/oauth-authorized')
@facebook_oauth.authorized_handler
def oauth_authorized(resp):
    facebook_graph = facebook.GraphAPI(resp.get('access_token'))
    email = facebook_graph.get_object("me")['email']
    sts_connection = STSConnection()
    role = sts_connection.assume_role(
        role_arn="arn:aws:iam::054060359478:role/facebook-login",
        role_session_name=email
    )
    creds = {
        'sessionId': role.credentials.access_key,
        'sessionKey': role.credentials.secret_key,
        'sessionToken': role.credentials.session_token
    }
    params = {
        'Action': 'getSigninToken',
        'Session': json.dumps(creds),
    }
    auth_url = "https://signin.aws.amazon.com/federation"
    r = requests.get(auth_url, params=params)
    signin_token = json.loads(r.text).get('SigninToken')
    params.update({
        'Action': 'login',
        'Issuer': 'ranman.org',
        'Destination': 'https://console.aws.amazon.com/',
        'SigninToken': signin_token
    })
    url = requests.Request('GET', auth_url, params=params).prepare().url
    return redirect(url)


@app.route('/')
def home_page():
    events = list(db.events.find().sort("date", -1))
    index = 0
    for index in range(len(events)):
        if events[index].get('date').replace(tzinfo=None) <= datetime.now():
            break
    upcoming = events[:index]
    past = events[index:]
    return render_template('ranman.html', upcoming=upcoming, past=past)


if __name__ == '__main__':
    app.run()
