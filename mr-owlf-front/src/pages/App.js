import React from 'react';
import { Switch, Route, Redirect, useRouteMatch } from "react-router-dom";

import Footer from '../components/Footer'
import Header from '../components/Header'

import Samples from './Samples'
import Statistics from './Statistics'
import TryOut from './TryOut'

function App() {

    let { path } = useRouteMatch();  

    return (
        <div className='card'>
            <Header />
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
                    <Route path={`${path}/*`} >
                        <Redirect from={`${path}/*`} to='/app' />
                    </Route>
                </Switch>
            </div>
            <Footer />
        </div>
    );
}

export default App;
