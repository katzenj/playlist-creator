from dotenv import load_dotenv
import json
import os
import requests

from .auth import SpotifyClientCredentials, SpotifyOauth


class PlaylistGenerator:
    def __init__(self):
        load_dotenv()
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        redirect_uri = 'http://localhost:5000/callback/'
        scope = 'playlist-modify-public playlist-modify-private'
        self._spotify_user_id = os.getenv('SPOTIFY_USER_ID')

        self._client_credentials = SpotifyClientCredentials(client_id, client_secret)
        self._spotify_oauth = SpotifyOauth(client_id, client_secret, redirect_uri, scope)

    def create_playlist(self, name, desc=None, public=False):
        # type: (str, Optional[str], bool) -> str, str
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self._spotify_user_id)
        access_token = self._spotify_oauth.get_access_token()

        body = json.dumps({
            'name': name,
            'description': desc,
            'public': False,
        })
        response = requests.post(
            url,
            data=body,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(access_token)
            }
        )
        # TODO: Error Handling

        response_json = response.json()
        return response_json['id'], response_json['owner']['id']


    def add_songs_to_playlist(self, playlist_id, artists):
        url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
        song_uris = []

        spotify_oauth_token = self._spotify_oauth.get_access_token()

        for artist in artists:
            artist_id = self.get_artist(artist)
            song_uris.append(self.get_songs_for_artist(artist_id))

        body_json = json.dumps({
            'uris': [song for song_list in song_uris for song in song_list],
        })

        response = requests.post(
            url,
            data=body_json,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(spotify_oauth_token)
            }
        )


    def get_artist(self, artist):
        formatted_name = artist.rstrip().replace(' ', '+')
        url = 'https://api.spotify.com/v1/search?q={}&type=artist'.format(formatted_name)

        response = requests.get(
            url,
            headers = {
                'Authorization': 'Bearer {}'.format(self._spotify_oauth.get_access_token())
            }
        )
        response_json = response.json()

        artists = response_json['artists']
        artist = artists['items'][0] if artists['items'] and len(artists['items']) > 0 else None
        return artist['id']


    def get_songs_for_artist(self, artist_id):
        # type: (str) -> List[str]
        url = 'https://api.spotify.com/v1/artists/{}/top-tracks?country=US'.format(artist_id)
        spotify_oauth_token = self._spotify_oauth.get_access_token()

        response = requests.get(
            url,
            headers = {
                'Authorization': 'Bearer {}'.format(spotify_oauth_token)
            }
        )
        response_json = response.json()
        tracks = response_json['tracks']
        return [track['uri'] for track in tracks]


    def get_spotify_auth_url(self):
        return self._spotify_oauth.get_authorize_url()

    def set_code(self, code):
        self._spotify_oauth.set_code(code)

def main():
    playlist_gen = PlaylistGenerator()
    playlist_id = playlist_gen.create_playlist('Testing 1234')
    playlist_gen.add_songs_to_playlist(playlist_id, ['Justin Bieber    ', 'Wiinston'])

if __name__ == '__main__':
    main()
