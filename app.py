from flask import Flask, render_template, request, redirect

from generator.generator import PlaylistGenerator

app = Flask(__name__)

gen = PlaylistGenerator()

@app.route('/')
def create_playlist():
    return render_template('create_playlist.html')


@app.route('/callback/')
def callback():
    return render_template('create_playlist.html')


@app.route('/spotify_login', methods=['GET'])
def spotify_login():
    response = gen.get_spotify_auth_url()
    return redirect(response)


@app.route('/submit_artist_data', methods=['POST'])
def submit_artists_data():
    artists_input: str = request.form.get('artists')
    playlist_title: str = request.form.get('playlist-title') or 'New Playlist'

    if artists_input is not None:
        id: str = gen.create_playlist(playlist_title)
        gen.add_songs_to_playlist(id, artists_input.split(','))
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
