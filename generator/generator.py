import base64
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import os
import requests

class PlaylistGenerator:
    def __init__(self):
        load_dotenv()
        self._spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self._spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self._spotify_user_id = os.getenv('SPOTIFY_USER_ID')
        self._spotify_oauth_token = os.getenv('SPOTIFY_OAUTH_TOKEN')
        self._expiration_time = None
        self._access_token = None


    def get_access_token(self):
        if self._expiration_time and self._expiration_time > (datetime.now() + timedelta(seconds=1)):
            return self._access_token

        url = 'https://accounts.spotify.com/api/token'

        payload = {
            'grant_type': 'client_credentials'
        }

        auth_header = base64.b64encode((self._spotify_client_id + ':' + self._spotify_client_secret).encode('ascii'))
        headers = {'Authorization': 'Basic {}'.format(auth_header.decode('ascii'))}

        response = requests.post(url, data=payload, headers=headers)
        response_json = response.json()

        self._expiration_time = datetime.now() + timedelta(seconds=response_json.get('expires_in'))
        self._access_token = response_json.get('access_token')

        return self._access_token


    def get_spotify_auth_url(self):
        scope = 'playlist-modify-public playlist-modify-private' 
        url = 'https://accounts.spotify.com/authorize/?response_type={}&client_id={}&scope={}&redirect_uri={}'.format('code', self._spotify_client_id, scope, 'localhost:5000/callback/')
        return url


    def create_playlist(self, name, desc=None, public=False):
        # type: (str, Optional[str], bool) -> str
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self._spotify_user_id)
        access_token = self.get_access_token()

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
                'Authorization': 'Bearer {}'.format(self._spotify_oauth_token)
            }
        )
        response_json = response.json()
        return response_json['id']


    def add_songs_to_playlist(self, playlist_id, artists):
        url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
        song_uris = []

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
                'Authorization': 'Bearer {}'.format(self._spotify_oauth_token)
            }
        )


    def get_artist(self, artist):
        formatted_name = artist.rstrip().replace(' ', '+')
        url = 'https://api.spotify.com/v1/search?q={}&type=artist'.format(formatted_name)

        response = requests.get(
            url,
            headers = {
                'Authorization': 'Bearer {}'.format(self._spotify_oauth_token)
            }
        )
        response_json = response.json()

        artists = response_json['artists']
        artist = artists['items'][0] if artists['items'] and len(artists['items']) > 0 else None
        return artist['id']


    def get_songs_for_artist(self, artist_id):
        # type: (str) -> List[str]
        url = 'https://api.spotify.com/v1/artists/{}/top-tracks?country=US'.format(artist_id)

        response = requests.get(
            url,
            headers = {
                'Authorization': 'Bearer {}'.format(self._spotify_oauth_token)
            }
        )
        response_json = response.json()
        tracks = response_json['tracks']
        return [track['uri'] for track in tracks]


def main():
    playlist_gen = PlaylistGenerator()
    playlist_id = playlist_gen.create_playlist('Testing 1234')
    playlist_gen.add_songs_to_playlist(playlist_id, ['Justin Bieber    ', 'Wiinston'])

if __name__ == '__main__':
    main()
