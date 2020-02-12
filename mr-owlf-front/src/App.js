import React from 'react';
import { Switch, Route, NavLink, useRouteMatch } from "react-router-dom";

import { Icon } from 'antd';

import Samples from './pages/Samples'
import Statistics from './pages/Statistics'
import TryOut from './pages/TryOut'

import logo from './assets/logo.svg';

function App() {

  let { path, url } = useRouteMatch();  

  return (
    <div className='card'>
      <div className="header">
            <div className="logo">
                <img src={logo} alt="logo" />
                <h1>Mr. Owlf</h1>
            </div>
            <ul className="menu">
                <li>
                    <NavLink activeClassName='active' to={url} exact><Icon type="thunderbolt" />Try Out</NavLink>
                </li>
                <li>
                    <NavLink activeClassName='active' to={`${url}/samples`}><Icon type="fire" />Samples</NavLink>
                </li>
                <li>
                    <NavLink activeClassName='active' to={`${url}/statistics`}><Icon type="rocket" />Statistics</NavLink>
                </li>
            </ul>
      </div>
      <div className="content">
        <Switch>
          <Route exact path={path}>
            <TryOut />
          </Route>
          <Route path={`${path}/samples`} component={Samples}>
            <Samples />
          </Route>
          <Route path={`${path}/statistics`} component={Samples}>
            <Statistics />
          </Route>
        </Switch>
      </div>
      
      <div className="footer">
        <b>Mr. Owlf</b> is made with <Icon type="heart" theme="twoTone" twoToneColor="#eb2f96" /> in Brazil by <a href="https://github.com/avcaliani" target="_blank" rel="noopener noreferrer">@avcaliani</a>
      </div>
    </div>
  );
}

export default App;
