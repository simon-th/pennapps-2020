import random
import string
from operator import itemgetter
import math

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
track_data = []

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


# For getting list of playlists for user selection
@app.route('/get_playlists', methods=['GET'])
def get_playlists():
    if not logged_in:
        return None
    return sp.current_user_playlists()


'''
    After user selects playlists, retrieves track data from all those playlists
    Need some help getting names of the playlists from frontend
    Input: names of playlists from user
    Output: list of audio features of all tracks in given playlists
'''
@app.route('/get_track_data', methods=['GET'])
def get_track_data():
    global track_data
    if not logged_in:
        return None
    playlist_names = []  # TODO: Change with user input from frontend
    playlist_ids = [get_playlist_id_by_name(name, sp.current_user_playlists())
                    for name in playlist_names]
    for pl_id in playlist_ids:
        tracks = sp.playlist_items(pl_id, fields='track.id', additional_types=['track'])
        for tr in tracks:
            track_data.append(sp.audio_features(tr))
    return track_data


# TODO: change the playlist name to match final product
@app.route('/create_playlist', methods=['GET'])
def create_playlist():
    if not logged_in:
        return None

    user_id = sp.me()['id']
    gen_descr = "Autogenerated playlist based on the mood, colors, and vibe of your photo."
    sp.user_playlist_create(user_id, "Image to Music Playlist", public=False,
                            collaborative=False, description=gen_descr)
    playlist_id = get_playlist_id_by_name("Image to Music Playlist", sp.current_user_playlists())
    # sp.playlist_upload_cover(playlist_id, _) need base64 encoded jpg as second arg

    ''' Hook up values from image analysis here '''
    # songs = sort_songs(get_image_tempo(), get_image_danceability())
    # sp.playlist_add_items(playlist_id, songs)
    # return the playlist


'''
    Args:
        tr_data - list of audio features of all songs
        image_tempo - float value of image analysis transformed into tempo
        image_danceability - float value of danceability
    Output - list of all track uris sorted.
    Can scale to multiple image properties given we change to L2 distance.
'''
def sort_songs(image_tempo, image_danceability):
    global track_data
    for feature in track_data:
        feature['tempo'] = math.sqrt(math.pow((feature['tempo']-image_tempo), 2) +
                                     math.pow(feature['danceability']-image_danceability, 2))
    track_data = sorted(track_data, key=itemgetter('tempo'))
    return [track_data[x]['uri'] for x in range(0, len(track_data))]


# Gets a playlist id by the name from a set of playlists
def get_playlist_id_by_name(name, playlists):
    for playlist in playlists['items']:
        if playlist['name'] == name:
            return playlist['id']


def generate_random_string(length):
    choices = string.ascii_letters + string.digits
    return ''.join(random.choice(choices) for i in range(length))
