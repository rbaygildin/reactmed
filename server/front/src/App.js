import React, { Component } from 'react';
import {BrowserRouter as Router, Route} from 'react-router-dom';
import Index from "./Index/Index";

class App extends Component {
  render() {
    return (
      <Router>
          <Route exact path="/" component={Index}/>
      </Router>
    );
  }
}

export default App;
