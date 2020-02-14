import React from 'react';
import { NavLink, useRouteMatch } from "react-router-dom";
import { Icon } from 'antd';

import logo from '../../assets/logo.svg';
import './styles.scss'

function Header() {

    let { url } = useRouteMatch();  

    return (
        <div className="header">
            <div className="logo">
                <img src={logo} alt="logo" />
                <h1>Mr. Owlf</h1>
            </div>
            <ul className="menu">
                <li>
                    <NavLink activeClassName='active' to={url} exact>
                        <Icon type="thunderbolt" />Try Out
                    </NavLink>
                </li>
                <li>
                    <NavLink activeClassName='active' to={`${url}/samples`}>
                        <Icon type="fire" />Samples
                    </NavLink>
                </li>
                <li>
                    <NavLink activeClassName='active' to={`${url}/statistics`}>
                        <Icon type="rocket" />Statistics
                    </NavLink>
                </li>
            </ul>
        </div>
    );
}

export default Header;
