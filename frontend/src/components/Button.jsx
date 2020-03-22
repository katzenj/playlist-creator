import classNames from 'classnames';
import React from 'react';
import PropTypes from 'prop-types';

import styles from 'src/components/main.css?module';

export const Button = ({ buttonText, onClick }) => (
  <div className={classNames({ [styles.input_group]: true, [styles.button_container]: true })}>
    <button
      className={styles.button}
      onClick={onClick}
    >
      {buttonText}
    </button>
  </div>
);

Button.propTypes = {
  buttonText: PropTypes.string,
  onClick: PropTypes.func
};
