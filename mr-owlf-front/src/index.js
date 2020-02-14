import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom'

import * as serviceWorker from './serviceWorker';

import './styles/index.scss';
import 'antd/dist/antd.css';

import App from './pages/App';

ReactDOM.render(
    <BrowserRouter>
        <Switch>
            <Route path="/" exact={true}>
                <Redirect from='/' to='/app' />
            </Route>
            <Route path="/app" component={App} />
            <Route path="*" >
                <Redirect from='*' to='/app' />
            </Route>
        </Switch>
    </ BrowserRouter>,
    document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
