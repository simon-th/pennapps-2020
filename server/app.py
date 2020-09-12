import random
import string

import spotipy
import spotipy.util as util

from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

# Constants
RANDOM_STRING_LENGTH = 16
FRONTEND_URL = 'http://localhost:3000/'

# Global variables
state = ''
scope = 'playlist-read-collaborative playlist-modify-public playlist-read-private playlist-modify-private'
sp = ''
oauth = ''
logged_in = False

# Flask App
app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    if logged_in:
        return 'Hello %s!' % sp.current_user()['display_name']
    return 'Hello, World!'


@app.route('/login', methods=['GET'])
def login():
    global state
    global oauth
    state = generate_random_string(RANDOM_STRING_LENGTH)
    oauth = SpotifyOAuth(
        state=state,
        scope=scope,
        cache_path='./token_cache'
    )
    return redirect(oauth.get_authorize_url())


@app.route('/callback', methods=['GET'])
def callback():
    global sp
    global logged_in
    all_args = request.args.to_dict()
    oauth.get_access_token(code=all_args['code'])
    sp = spotipy.Spotify(auth_manager=oauth)
    logged_in = True
    return redirect(FRONTEND_URL + '?login=y')


@app.route('/logout', methods=['GET'])
def logout():
    global state
    global oauth
    global sp
    global logged_in
    state = ''
    oauth = ''
    sp = ''
    logged_in = ''
    return redirect(FRONTEND_URL + '?logout=y')


@app.route('/get_user', methods=['GET'])
def get_user():
    if not logged_in:
        return None
    return sp.current_user()


def generate_random_string(length):
    choices = string.ascii_letters + string.digits
    return ''.join(random.choice(choices) for i in range(length))
