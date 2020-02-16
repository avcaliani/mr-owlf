import React from 'react';
import { Form, Input, DatePicker, Button, Icon, notification } from 'antd';

import verify from './service.js'
import './styles.scss';

const { TextArea } = Input;

class TryOutForm extends React.Component {

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            const ret = verify({
                ...values,
                'publish_date': values['publish_date'] ? values['publish_date'].format('YYYY-MM-DD') : undefined
            })
            this.notify(ret.title, ret.description, ret.icon, ret.iconColor)  
        });
    };

    notify = (title, desc, icon, iconColor) => {
        notification.open({
            message: title,
            description: desc,
            icon: <Icon type={icon} style={{ color: iconColor }} />,
        });
    };

    render() {
        const { getFieldDecorator } = this.props.form;

        return ( 
            <Form onSubmit={this.handleSubmit} className="try-out-form">

                <span><Icon type="team" />Authors</span>
                <Form.Item>
                    { getFieldDecorator('authors')(<Input placeholder="John Dale" />) }
                </Form.Item>

                <span><Icon type="cloud" />Domain</span>
                <Form.Item>
                    { getFieldDecorator('domain')(<Input placeholder="www.domain.com" />) }
                </Form.Item>

                <span><Icon type="calendar" />Published At</span>
                <Form.Item>
                    { getFieldDecorator('publish_date')(<DatePicker />) }
                </Form.Item>

                <span><Icon type="coffee" />News</span>
                <Form.Item>
                    { getFieldDecorator('news')(<TextArea rows={1} placeholder="I saw something that I don't know if it's fake..." />) }
                </Form.Item>
                <Form.Item>
                    <Button htmlType="submit" className="submit-button">Try Now</Button>
                </Form.Item>
            </Form>
        );
    }
}

const TryOut = Form.create({ name: 'try_out_form' })(TryOutForm);

export default TryOut;
