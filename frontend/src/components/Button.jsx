import classNames from 'classnames';
import React from 'react';
import PropTypes from 'prop-types';

import styles from 'src/components/main.css?module';

export const Button = ({ buttonText, onClick, disabled }) => (
  <div className={classNames({ [styles.input_group]: true, [styles.button_container]: true })}>
    <button
      disabled={disabled}
      className={styles.button}
      onClick={onClick}
    >
      {buttonText}
    </button>
  </div>
);

Button.propTypes = {
  buttonText: PropTypes.string.isRequired,
  onClick: PropTypes.func.isRequired,
  disabled: PropTypes.bool
};

Button.defaultProps = {
  disabled: false
};
