import base64
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import os
import requests
from urllib.parse import urlencode, quote


OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'


class SpotifyClientCredentials(object):
    def __init__(self, client_id=None, client_secret=None):
        load_dotenv()
        if not client_id:
            client_id = os.getenv('SPOTIFY_CLIENT_ID')

        if not client_secret:
            client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        self._client_id = client_id
        self._client_secret = client_secret
        self._access_token = None
        self._expiration_time = None


    def _get_auth_headers(self):
        auth_header = base64.b64encode((self._client_id + ':' + self._client_secret).encode('ascii'))
        return {'Authorization': 'Basic {}'.format(auth_header.decode('ascii'))}


    def _is_token_expired(self):
        return self._expiration_time and self._expiration_time < (datetime.now() + timedelta(seconds=1))


    def _request_access_token(self):
        payload = {
            'grant_type': 'client_credentials'
        }
        headers = self._get_auth_headers()
        response = requests.post(OAUTH_TOKEN_URL, data=payload, headers=headers)
        response_json = response.json()

        expiration_time = datetime.now() + timedelta(seconds=response_json.get('expires_in'))
        access_token = response_json.get('access_token')
        return access_token, expiration_time


    def get_access_token(self):
        if self._access_token and not self._is_token_expired():
            return self._access_token

        access_token, expiration = self._request_access_token()
        self._access_token = access_token
        self._expiration = expiration

        return self._access_token


class SpotifyOauth(object):
    def __init__(self, client_id, client_secret, redirect_uri, scope=None):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._scope = scope
        self._access_token = None
        self._expiration_time = None


    def _get_auth_headers(self):
        auth_header = base64.b64encode((self._client_id + ':' + self._client_secret).encode('ascii'))
        return {'Authorization': 'Basic {}'.format(auth_header.decode('ascii'))}


    def _is_token_expired(self):
        return self._expiration_time and self._expiration_time < (datetime.now() + timedelta(seconds=1))


    def get_authorize_url(self):
        response_type = 'code'
        url = 'https://accounts.spotify.com/authorize?response_type={}&client_id={}&redirect_uri={}&scope={}'.format(response_type, self._client_id, quote(self._redirect_uri), quote(self._scope))
        return url


    def set_code(self, code):
        self._code = code


    def get_access_token(self):
        if self._access_token and not self._is_token_expired():
            return self._access_token

        if self._access_token and self.is_token_expired():
            return self.get_refresh_token()

        payload = {
            'redirect_uri': self._redirect_uri,
            'code': self._code,
            'grant_type': 'authorization_code'
        }

        if self._scope:
            payload['scope'] = quote(self._scope)

        headers = self._get_auth_headers()

        response = requests.post(
            OAUTH_TOKEN_URL,
            data=payload,
            headers=headers,
            verify=True
        )

        # TODO: Error Handling.
        response_json = response.json()

        self._expiration_time = datetime.now() + timedelta(seconds=response_json.get('expires_in'))
        self._access_token = response_json.get('access_token')
        self._refresh_token = response_json.get('refresh_token')

        return self._access_token


    def get_refresh_token(self):
        payload = {
            'refresh_token': self._refresh_token,
            'grant_type': 'refresh_token'
        }
        headers = self._get_auth_headers()
        response = requests.post(
            OAUTH_TOKEN_URL,
            data=payload,
            headers=headers
        )

        response_json = response.json()

        expiration_time = datetime.now() + timedelta(seconds=response_json.get('expires_in'))
        access_token = response_json.get('access_token')
        self._expiration_time = expiration_time
        self._access_token = access_token
        self._refresh_token = refresh_token

        return access_token


