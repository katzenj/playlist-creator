import React from 'react';
import PropTypes from 'prop-types';
import styles from './main.css?module';

export const InputGroup = ({ name, placeholder }) => (
  <div className={styles.input_group} id={`${name}-container`}>
    <input
      className={styles.input}
      type="text"
      name={name}
      id={`${name}-id`}
      placeholder={placeholder}
      aria-label={placeholder}
      aria-describedby="title-input-label"
    />
  </div>
);

InputGroup.propTypes = {
  name: PropTypes.string,
  placeholder: PropTypes.string
};
