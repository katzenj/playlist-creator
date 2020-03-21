import React from 'react';
import { InputGroup } from '../components/InputGroup';

import styles from '../styles/main.css?module';

export const GeneratorPage = () => {
  return (
    <div>
      <div className={styles.content_container}>
        <h1 className={styles.header}>Generate a Playlist!</h1>
        <InputGroup name="playlist-title" placeholder="Playlist Title" />
        <InputGroup name="artists" placeholder="Artists" />
        <InputGroup name="songs" placeholder="Songs" />
      </div>
    </div>
  );
};

