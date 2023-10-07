import { Avatar, Button, Col, Drawer, Layout, Menu, Row, theme, Typography } from 'antd';
import React, { useState } from 'react';
import { Link, Outlet } from 'react-router-dom';

import {
    DashboardOutlined,
    UserOutlined,
    LogoutOutlined,
    PlusCircleOutlined,
    ShoppingOutlined,
    MenuOutlined,
} from '@ant-design/icons';

import type { MenuProps } from 'antd';
import MediaQuery from 'react-responsive';
import AuthService from '../api/AuthService';

const { Header, Content, Sider } = Layout;

const logout = () => {
    AuthService.logout();

    setTimeout(() => {
        window.location.href = '/login';
    }, 100);
};

const menuItems: MenuProps['items'] = [
    {
        label: <Link to='/dashboard/profile'>Мой кабинет</Link>,
        icon: React.createElement(DashboardOutlined),
        key: 'profile',
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

const mobileMenuItems = menuItems.concat([
    {
        label: (
            <Link
                onClick={() => {
                    AuthService.logout();

                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 100);
                }}
                to='/login'
            >
                Выйти
            </Link>
        ),
        icon: React.createElement(LogoutOutlined),
        key: 'logout',
    },
]);

const desktopSize = '(min-width: 1024px)';
const mobileSize = '(max-width: 1024px)';

const DashboardLayout: React.FC = () => {
    const {
        token: { colorBgContainer },
    } = theme.useToken();
    const [open, setOpen] = useState(false);

    const showDrawer = () => {
        setOpen(true);
    };

    const onClose = () => {
        setOpen(false);
    };

    return (
        <Layout className='dashboard-layout'>
            <Header className='header'>
                <Typography.Title level={3} className='logo'>
                    MISIS Gis
                </Typography.Title>

                <Col>
                    <MediaQuery query={desktopSize}>
                        <Avatar style={{ backgroundColor: '#666' }} icon={<UserOutlined />} />

                        <span style={{ marginLeft: 10, marginRight: 20, color: '#fff' }}>
                            {`${
                                AuthService.getCurrentUser()?.user?.name ??
                                AuthService.getCurrentUser()?.user.name
                            }`}
                        </span>

                        <Link onClick={logout} to='/login' style={{ color: '#fff' }}>
                            Выйти <LogoutOutlined style={{ color: '#fff' }} />
                        </Link>
                    </MediaQuery>
                    <MediaQuery query={mobileSize}>
                        <Button
                            type='primary'
                            onClick={showDrawer}
                            icon={<MenuOutlined />}
                        ></Button>
                    </MediaQuery>
                </Col>
            </Header>
            <Layout>
                <MediaQuery query={desktopSize}>
                    <Sider width={200} style={{ background: colorBgContainer }}>
                        <Menu
                            mode='inline'
                            defaultSelectedKeys={['profile']}
                            defaultOpenKeys={['profile']}
                            style={{ height: '100%', borderRight: 0 }}
                            items={menuItems}
                        />
                    </Sider>
                </MediaQuery>
                <MediaQuery query={mobileSize}>
                    <Drawer title='Меню' placement='right' onClose={onClose} open={open}>
                        <Row align={'middle'} style={{ marginBottom: 20 }}>
                            <Avatar
                                style={{ backgroundColor: '#666', marginLeft: 20 }}
                                icon={<UserOutlined />}
                            />

                            <span style={{ marginLeft: 10 }}>
                                {`${
                                    AuthService.getCurrentUser()?.user?.name ??
                                    AuthService.getCurrentUser()?.user.name
                                }`}
                            </span>
                        </Row>

                        <Menu
                            mode='inline'
                            defaultSelectedKeys={['profile']}
                            defaultOpenKeys={['profile']}
                            style={{ height: '100%', borderRight: 0 }}
                            items={mobileMenuItems}
                            onSelect={() => {
                                setOpen(false);
                            }}
                        />
                    </Drawer>
                </MediaQuery>
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
