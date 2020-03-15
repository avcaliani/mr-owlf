import React from 'react';
import Axios from 'axios';
import { Form, Input, DatePicker, Button, Icon, notification } from 'antd';

import service from './service.js'
import './styles.scss';

const { TextArea } = Input;

class TryOutForm extends React.Component {

    handleSubmit = e => {
        e.preventDefault();
        this.props.form.validateFields((err, values) => {
            Axios.post(`${process.env.REACT_APP_API}/score`, {
                ...values,
                'publish_date': values['publish_date'] ? values['publish_date'].format('YYYY-MM-DD') : undefined
            })
            .then(response => this.notify(service.verify(response.data)))
            .catch(err => {
                const status = err && err.response ? err.response.status : 'NO_NETWORK';
                this.notify(service.verifyError(status))
            });
        });
    };

    notify = data => notification.open({
        message: data.title,
        description: data.description,
        icon: <Icon type={ data.icon } style={{ color: data.iconColor }} />,
        duration: 15
    });

    render() {
        const { getFieldDecorator } = this.props.form;
        return ( 
            <Form onSubmit={this.handleSubmit} className="try-out-form">

                <span><Icon type="team" />Author</span>
                <Form.Item>
                    { getFieldDecorator('author')(<Input placeholder="John Dale" />) }
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
                    { getFieldDecorator('sentence')(<TextArea rows={1} placeholder="I saw something that I don't know if it's fake..." />) }
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
