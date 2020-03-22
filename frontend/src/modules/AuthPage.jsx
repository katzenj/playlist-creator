import React from 'react';

import { Button } from 'src/components/Button';
import styles from 'src/modules/main.css?module';

export const AuthPage = () => {
  const cookie = 'test_cookie_1';

  const setCookie = () => {
    const exp = new Date();
    const time = exp.getTime() + (3600 * 1000);
    exp.setTime(time);
    document.cookie = `spotify_cookie=${cookie}; expires=${exp.toUTCString()};p path="/"`;
  };

  const getSpotifyAuthUrl = async () => {
    setCookie();
    const url = '/api/spotify_login';
    const options = {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8'
      }
    };
    const response = await fetch(url, options);
    const json = await response.json();
    window.location.href = `${json.spotify_url}&state=${cookie}`;
  };

  return (
    <div>
      <div className={styles.content_container}>
        <h1 className={styles.header}>Generate a Playlist!</h1>
        <Button
          buttonText="Authorize Spotify"
          onClick={() => getSpotifyAuthUrl()}
        />
      </div>
    </div>
  );
};
