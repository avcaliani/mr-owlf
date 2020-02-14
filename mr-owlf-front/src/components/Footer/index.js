import React from 'react';
import { Icon } from 'antd';

import './styles.scss'

function Footer() {
    return (
        <div className="footer">
            <b>Mr. Owlf</b> is made with <Icon type="heart" theme="twoTone" twoToneColor="#eb2f96" /> in Brazil by <a href="https://github.com/avcaliani" target="_blank" rel="noopener noreferrer">@avcaliani</a>
        </div>
    );
}

export default Footer;
