import React from 'react';
import ReactDOM from 'react-dom';
import { GeneratorPage } from './modules/GeneratorPage';

const App = () => {
  return (
    <GeneratorPage />
  );
};

ReactDOM.render(<App />, document.getElementById('root'));
