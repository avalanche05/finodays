import { Avatar, Col, Layout, Menu, theme, Typography } from 'antd';
import React from 'react';
import { Link, Outlet } from 'react-router-dom';

import {
    DashboardOutlined,
    FormOutlined,
    UserOutlined,
    LogoutOutlined,
    PlusCircleOutlined,
    ShoppingOutlined,
} from '@ant-design/icons';

import type { MenuProps } from 'antd';
import AuthService from '../api/AuthService';
const { Header, Content, Sider } = Layout;

const menuItems: MenuProps['items'] = [
    {
        label: <Link to='/dashboard/profile'>Мой кабинет</Link>,
        icon: React.createElement(DashboardOutlined),
        key: 'profile',
    },
    {
        label: <Link to='/dashboard/my-cfas'>Мои ЦФА</Link>,
        icon: React.createElement(FormOutlined),
        key: 'my-cfas',
    },
    {
        label: <Link to='/dashboard/create-cfa'>Создать ЦФА</Link>,
        icon: React.createElement(PlusCircleOutlined),
        key: 'create-cfa',
    },
    {
        label: <Link to='/dashboard/cfa-market'>Витрина ЦФА</Link>,
        icon: React.createElement(ShoppingOutlined),
        key: 'cfa-market',
    },
];

const DashboardLayout: React.FC = () => {
    const {
        token: { colorBgContainer },
    } = theme.useToken();

    return (
        <Layout className='dashboard-layout'>
            <Header className='header'>
                <Typography.Title level={3} className='logo'>
                    MISIS Gis
                </Typography.Title>

                <Col>
                    <Avatar style={{ backgroundColor: '#666' }} icon={<UserOutlined />} />

                    <span style={{ marginLeft: 10, color: '#fff' }}>АО Ромашка</span>

                    <Link
                        onClick={() => {
                            AuthService.logout();

                            setTimeout(() => {
                                window.location.href = '/login';
                            }, 100);
                        }}
                        to='/login'
                        style={{ marginLeft: 20 }}
                    >
                        <LogoutOutlined style={{ color: '#fff' }} />
                    </Link>
                </Col>
            </Header>
            <Layout>
                <Sider width={200} style={{ background: colorBgContainer }}>
                    <Menu
                        mode='inline'
                        defaultSelectedKeys={['profile']}
                        defaultOpenKeys={['profile']}
                        style={{ height: '100%', borderRight: 0 }}
                        items={menuItems}
                    />
                </Sider>
                <Layout style={{ padding: '24px 24px 24px' }}>
                    <Content
                        style={{
                            padding: 24,
                            margin: 0,
                            minHeight: 280,
                            background: colorBgContainer,
                        }}
                    >
                        <Outlet />
                    </Content>
                </Layout>
            </Layout>
        </Layout>
    );
};

export default DashboardLayout;
