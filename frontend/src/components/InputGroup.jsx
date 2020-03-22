import React from 'react';
import PropTypes from 'prop-types';
import styles from 'src/components/main.css?module';

export const InputGroup = ({ name, placeholder, onChange }) => (
  <div className={styles.input_group} id={`${name}-container`}>
    <input
      className={styles.input}
      type="text"
      name={name}
      id={`${name}-id`}
      placeholder={placeholder}
      aria-label={placeholder}
      aria-describedby="title-input-label"
      onChange={(e) => {
        onChange(e.target.value);
      }}
    />
  </div>
);

InputGroup.propTypes = {
  name: PropTypes.string.isRequired,
  onChange: PropTypes.func.isRequired,
  placeholder: PropTypes.string.isRequired
};
