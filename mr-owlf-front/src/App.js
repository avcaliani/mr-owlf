import React from 'react';
import { Switch, Route, NavLink, useRouteMatch } from "react-router-dom";
import Samples from './components/Samples'
import Statistics from './components/Statistics'
import logo from './logo.svg';
import './App.css';

function App() {

  let { path, url } = useRouteMatch();  

  return (
    <div className="App">
      <header className="App-header">

        <img src={logo} className="App-logo" alt="logo" />

        <Switch>
          <Route exact path={path}>
            <h3>Try Out</h3>
          </Route>
          <Route path={`${path}/samples`} component={Samples}>
            <Samples />
          </Route>
          <Route path={`${path}/statistics`} component={Samples}>
            <Statistics />
          </Route>
        </Switch>
        
        <NavLink activeClassName='is-active' to={`${url}`} exact>Try Out</NavLink>
        <NavLink activeClassName='is-active' to={`${url}/samples`}>Samples</NavLink>
        <NavLink activeClassName='is-active' to={`${url}/statistics`}>Statistics</NavLink>
      </header>
    </div>
  );
}

export default App;
