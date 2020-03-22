from dotenv import load_dotenv
import json
import os
import requests
from typing import List, Optional

from .auth import SpotifyClientCredentials, SpotifyOauth


class PlaylistGenerator:
    def __init__(self):
        load_dotenv()
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        redirect_uri = 'http://localhost:8080/spotify_callback'
        scope = 'playlist-modify-public playlist-modify-private'
        self._spotify_user_id = os.getenv('SPOTIFY_USER_ID')

        self._client_credentials = SpotifyClientCredentials(client_id, client_secret)
        self._spotify_oauth = SpotifyOauth(client_id, client_secret, redirect_uri, scope)

    def create_playlist(self, name: str, desc: Optional[str]=None, public: Optional[bool]=False) -> (str, str):
        url = 'https://api.spotify.com/v1/users/{}/playlists'.format(self._spotify_user_id)
        access_token = self._spotify_oauth.get_access_token()

        body = json.dumps({
            'name': name,
            'description': desc,
            'public': public,
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


    def add_songs_to_playlist(self, playlist_id: str, artists: List[str]):
        url = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(playlist_id)
        spotify_oauth_token = self._spotify_oauth.get_access_token()

        song_uris = []
        artist_ids = []
        for artist in artists:
            artist_id = self.get_artist(artist)
            artist_ids.append(artist_id)
            song_uris.append(self.get_songs_for_artist(artist_id))

        song_uris.append(self.get_recommended_tracks_for_artists(artist_ids))

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


    def get_artist(self, artist: str) -> str:
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


    def get_songs_for_artist(self, artist_id: str) -> List[str]:
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

        if len(tracks) > 5:
            return [track['uri'] for track in tracks[:5]]

        return [track['uri'] for track in tracks]

    def get_recommended_tracks_for_artists(self, artist_ids: List[str]) -> List[str]:
        url = 'https://api.spotify.com/v1/recommendations?seed_artists={}&market=US'.format(','.join(artist_ids))
        spotify_oauth_token = self._spotify_oauth.get_access_token()

        response = requests.get(
            url,
            headers = {
                'Authorization': 'Bearer {}'.format(spotify_oauth_token)
            }
        )
        response_json = response.json()
        return [track['uri'] for track in response_json['tracks']]


    def get_spotify_auth_url(self):
        return self._spotify_oauth.get_authorize_url()

    def set_code(self, code: str):
        self._spotify_oauth.set_code(code)
