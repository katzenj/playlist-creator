import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import { AuthPage } from 'src/modules/AuthPage';
import { GeneratorPage } from 'src/modules/GeneratorPage';

const App = () => {
  return (
    <Router>
      <Route exact path="/" component={AuthPage} />
      <Route path="/spotify_callback" component={GeneratorPage} />
    </Router>
  );
};

export default App;
