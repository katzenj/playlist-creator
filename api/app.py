from flask import Flask, jsonify, render_template, request, redirect, url_for
import time

from generator.generator import PlaylistGenerator

app = Flask(__name__)

gen = PlaylistGenerator()
playlists = []
NUM_PLAYLISTS = 3

@app.route('/')
def create_playlist():
    return render_template('auth.html')


@app.route('/callback/')
def callback():
    gen.set_code(request.args.get('code'))
    return render_template('create_playlist.html')

@app.route('/spotify_login_2', methods=['GET'])
def spotify_login_2():
    response = gen.get_spotify_auth_url()
    return jsonify({'spotify_url': response})

@app.route('/spotify_login', methods=['GET'])
def spotify_login():
    response = gen.get_spotify_auth_url()
    return redirect(response)


@app.route('/submit_artist_data', methods=['POST'])
def submit_artists_data():
    artists_input: str = request.form.get('artists')
    playlist_title: str = request.form.get('playlist-title') or 'New Playlist'

    if artists_input is not None:
        playlist_id, user_id = gen.create_playlist(playlist_title)
        gen.add_songs_to_playlist(playlist_id, artists_input.split(','))

        return redirect(url_for('view_playlist', playlist_id=playlist_id, user_id=user_id))

    return redirect(url_for('create_playlist'))


@app.route('/view_playlist/<user_id>/<playlist_id>')
def view_playlist(playlist_id, user_id):
    # type: (str) -> ()
    playlist_url = 'https://open.spotify.com/embed/user/{}/playlist/{}'.format(user_id, playlist_id)
    if playlist_url not in playlists:
        playlists.append(playlist_url)
    return render_template('create_playlist.html', playlists=playlists[-1 * NUM_PLAYLISTS:])


if __name__ == '__main__':
    app.run(debug=True)
