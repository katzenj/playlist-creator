import React, { useState, useEffect } from 'react';
import { InputGroup } from 'src/components/InputGroup';
import { Button } from 'src/components/Button';

import styles from 'src/modules/main.css?module';

export const GeneratorPage = () => {
  const [playlistTitle, setPlaylistTitle] = useState(null);
  const [artists, setArtists] = useState(null);
  const [songs, setSongs] = useState(null);
  const [playlistData, setPlaylistData] = useState({ userId: null, playlistIds: [] });

  const getUrlParameter = (name) => {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
  };

  const setSpotifyCode = async (code) => {
    const url = '/api/set_spotify_code';
    const options = {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      body: JSON.stringify({ spotify_code: code })
    };
    const result = await fetch(url, options);
    // TODO: Ensure 200 status/do error handling.
    await result.json();
  };

  const createPlaylist = async (createPlaylistData) => {
    const url = '/api/submit_playlist_data';
    const options = {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json;charset=UTF-8'
      },
      body: JSON.stringify(createPlaylistData)
    };
    const result = await fetch(url, options);
    // TODO: Ensure 200 status/do error handling.
    const json = await result.json();
    const playlistIds = playlistData.playlistIds;
    playlistIds.push(json.response.playlist_id);

    setPlaylistData({
      userId: json.response.user_id,
      playlistIds
    });
  };

  useEffect(() => {
    // TODO: CHECK cookie/state param to ensure that it's the same user.
    // TODO: Add encryption to code.
    setSpotifyCode(getUrlParameter('code'));
  });

  const createPlaylistUrl = (playlistId) => (
    `https://open.spotify.com/embed/user/${playlistData.userId}/playlist/${playlistId}`
  );

  return (
    <div>
      <div className={styles.content_container}>
        <h1 className={styles.header}>Generate a Playlist!</h1>
        <div className={styles.playlist_inputs_container}>
          <InputGroup
            name="playlist-title"
            placeholder="Playlist Title"
            onChange={setPlaylistTitle}
          />
          <InputGroup
            name="artists"
            placeholder="Artists"
            onChange={setArtists}
          />
          <InputGroup name="songs" placeholder="Songs" onChange={setSongs} />
        </div>
        <Button
          buttonText="Create a Playlist"
          onClick={() =>
            createPlaylist({ playlist_title: playlistTitle, artists, songs })
          }
        />
        <div className={styles.embed_container}>
          {playlistData.playlistIds.length > 0 && playlistData.playlistIds.map((id) => (
            <iframe
              className={styles.spotify_embed}
              key={id}
              id={`playlist-${id}-iframe`}
              src={createPlaylistUrl(id)}
              width="300"
              height="500"
              frameBorder="0"
              allowtransparency="true"
            />
          ))}
        </div>
      </div>
    </div>
  );
};

