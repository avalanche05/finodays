import { Button, Checkbox, Col, Form, Input, Row, Typography } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { Link } from 'react-router-dom';

const Login = () => {
    const onFinish = (values: unknown) => {
        console.log('Received values of form: ', values);
    };

    return (
        <Row className='auth'>
            <Col span={6} xs={{ span: 20 }} lg={{ span: 6 }}>
                <Typography.Title style={{ textAlign: 'center' }} level={2}>
                    MISIS Gis
                </Typography.Title>
                <Typography.Paragraph type='secondary' style={{ textAlign: 'center' }}>
                    Начните работу с ЦФА вместе с нами!
                </Typography.Paragraph>
                <Form
                    style={{ marginTop: 50 }}
                    name='login'
                    initialValues={{
                        remember: true,
                    }}
                    onFinish={onFinish}
                >
                    <Form.Item
                        name='username'
                        rules={[
                            {
                                required: true,
                                message: 'Пожалуйста, введите имя пользователя или email',
                            },
                        ]}
                    >
                        <Input
                            size='large'
                            prefix={<UserOutlined className='site-form-item-icon' />}
                            placeholder='Имя пользователя или email'
                        />
                    </Form.Item>
                    <Form.Item
                        name='password'
                        rules={[
                            {
                                required: true,
                                message: 'Пожалуйста, введите пароль',
                            },
                        ]}
                    >
                        <Input
                            size='large'
                            prefix={<LockOutlined className='site-form-item-icon' />}
                            type='password'
                            placeholder='Пароль'
                        />
                    </Form.Item>
                    <Form.Item>
                        <Form.Item name='remember' valuePropName='checked' noStyle>
                            <Checkbox>Запомнить меня</Checkbox>
                        </Form.Item>

                        <Link to={'/signup'}>Еще нет аккаунта</Link>
                    </Form.Item>

                    <Form.Item>
                        <Button
                            block
                            type='primary'
                            htmlType='submit'
                            className='login-form-button'
                            size='large'
                        >
                            Войти
                        </Button>
                    </Form.Item>
                </Form>
            </Col>
        </Row>
    );
};

export default Login;
