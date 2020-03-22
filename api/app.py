from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, redirect, session, url_for
import os
import random
import string
import time

from generator.generator import PlaylistGenerator

app = Flask(__name__)

gen = PlaylistGenerator()
playlists = []
NUM_PLAYLISTS = 3

def _create_cookie(length: int=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for n in range(length))


@app.route('/api/spotify_login', methods=['GET'])
def new_spotify_login():
    spotify_url = gen.get_spotify_auth_url()
    spotify_cookie = _create_cookie(length=16)
    session['spotify_cookie'] = spotify_cookie
    return jsonify({'spotify_url': spotify_url})


@app.route('/api/set_spotify_code', methods=['POST'])
def new_set_spotify_code():
    data = request.json;
    gen.set_code(data['spotify_code'])
    return jsonify({'status_code': 200, 'message': 'Successfully set code.'})


@app.route('/api/submit_playlist_data', methods=['POST'])
def new_submit_playlist_data():
    data = request.json
    print(data)
    artists_input: str = data['artists']
    playlist_title: str = data.get('playlist_title', 'New Playlist')

    if artists_input is not None:
        playlist_id, user_id = gen.create_playlist(playlist_title)
        gen.add_songs_to_playlist(playlist_id, artists_input.split(','))

        return jsonify({
            'status_code': 200, 
            'response': {
                'playlist_id': playlist_id, 'user_id': user_id
            }
        })

    return jsonify({'status_code': 400, 'message': 'Add artists data to create a playlist.'})


if __name__ == '__main__':
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')
    app.run(debug=True)
