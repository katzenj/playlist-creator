import React, { useState } from 'react';
import { InputGroup } from '../components/InputGroup';
import { Button } from '../components/Button';

import styles from '../styles/main.css?module';

export const GeneratorPage = () => {
  const [playlistTitle, setPlaylistTitle] = useState(null);
  const [artists, setArtists] = useState(null);
  const [songs, setSongs] = useState(null);

  const getSpotifyAuthUrl = async () => {
    const url = '/api/spotify_login_2';
    const options = {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8'
      }
    };
    const response = await fetch(url, options);
    const json = await response.json();
    return json.spotify_url;
  };

  return (
    <div>
      <div className={styles.content_container}>
        <h1 className={styles.header}>Generate a Playlist!</h1>
        <Button buttonText="Authorize Spotify" onClick={() => {
          getSpotifyAuthUrl();
        }} />
        <InputGroup name="playlist-title" placeholder="Playlist Title" onChange={setPlaylistTitle} />
        <InputGroup name="artists" placeholder="Artists" onChange={setArtists} />
        <InputGroup name="songs" placeholder="Songs" onChange={setSongs} />
        <Button buttonText="Create a Playlist" onClick={() => console.log({ playlistTitle, artists, songs })} />
      </div>
    </div>
  );
};

