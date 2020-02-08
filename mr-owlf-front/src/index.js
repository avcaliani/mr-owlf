import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom'
import * as serviceWorker from './serviceWorker';
import './styles/index.scss';
import App from './App';
import NotFound from './pages/NotFound';

ReactDOM.render(
    <BrowserRouter>
        <Switch>
            <Route path="/" exact={true}>
                <Redirect from='/' to='/app' />
            </Route>
            <Route path="/app" component={App} />
            <Route path="*" component={NotFound} />
        </Switch>
    </ BrowserRouter>,
    document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();