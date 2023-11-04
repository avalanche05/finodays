import { Avatar, Col, Layout, Menu, theme, Typography } from 'antd';
import { Link, Outlet, useLocation, useNavigate } from 'react-router-dom';

import {
    UserOutlined,
    LogoutOutlined,
    PlusCircleOutlined,
    ShoppingOutlined,
} from '@ant-design/icons';

import MediaQuery from 'react-responsive';
import AuthService from '../api/AuthService';
import { TabBar } from 'antd-mobile';

const { Header, Content, Sider } = Layout;

const logout = () => {
    AuthService.logout();

    setTimeout(() => {
        window.location.href = '/login';
    }, 100);
};

const menuItems = [
    {
        key: '/dashboard/profile',
        label: 'Мой кабинет',
        icon: <UserOutlined />,
    },
    {
        key: '/dashboard/create-cfa',
        label: 'Создать ЦФА',
        icon: <PlusCircleOutlined />,
    },
    {
        key: '/dashboard/cfa-market',
        label: 'Витрина ЦФА',
        icon: <ShoppingOutlined />,
    },
];

const desktopSize = '(min-width: 1024px)';
const mobileSize = '(max-width: 1024px)';

const DashboardLayout: React.FC = () => {
    const {
        token: { colorBgContainer },
    } = theme.useToken();
    const navigate = useNavigate();
    const location = useLocation();

    const setRouteActive = (value: string) => {
        navigate(value);
    };

    return (
        <Layout className='dashboard-layout'>
            <Header className='header'>
                <Typography.Title level={3} className='logo'>
                    <svg
                        width='1340'
                        height='177'
                        viewBox='0 0 1340 177'
                        fill='none'
                        xmlns='http://www.w3.org/2000/svg'
                        style={{ width: 150, position: 'relative', top: 3, left: -23 }}
                    >
                        <path
                            d='M35.2581 176.29H0V0H35.2581L96.7079 85.3749L159.165 0H193.164V176.29H157.906V57.4203L111.819 125.166H82.3528L35.2581 57.4203V176.29Z'
                            fill='white'
                        />
                        <path d='M253.654 176.29H218.396V0H253.654V176.29Z' fill='white' />
                        <path
                            d='M550.669 176.29H296.274L278.897 158.913V123.655H314.155V141.032H533.04V106.026H296.274L278.897 93.4339V17.8809L296.274 0H550.669L568.046 17.8809V52.8871H533.04V35.2581H314.155V70.5162H550.669L568.046 88.1452V158.913L550.669 176.29Z'
                            fill='white'
                        />
                        <path d='M628.372 176.29H593.114V0H628.372V176.29Z' fill='white' />
                        <path
                            d='M794.396 176.29H670.993L653.616 158.913V123.655H688.874V141.032H776.767V106.026H670.993L653.616 93.4339V17.8809L670.993 0H794.396L811.773 17.8809V52.8871H776.767V35.2581H688.874V70.5162H794.396L811.773 88.1452V158.913L794.396 176.29Z'
                            fill='white'
                        />
                        <path
                            d='M1078.46 176.29H955.055L937.677 158.913V17.8809L955.055 0H1078.46L1095.84 17.8809V52.8871H1060.83V35.2581H972.936V141.032H1060.83V110.559H1016.5V75.3012H1095.84V158.913L1078.46 176.29Z'
                            fill='white'
                        />
                        <path d='M1156.16 176.29H1120.9V0H1156.16V176.29Z' fill='white' />
                        <path
                            d='M1322.19 176.29H1198.78L1181.4 158.913V123.655H1216.66V141.032H1304.56V106.026H1198.78L1181.4 93.4339V17.8809L1198.78 0H1322.19L1339.56 17.8809V52.8871H1304.56V35.2581H1216.66V70.5162H1322.19L1339.56 88.1452V158.913L1322.19 176.29Z'
                            fill='white'
                        />
                    </svg>
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
                    </MediaQuery>

                    <Link onClick={logout} to='/login' style={{ color: '#fff' }}>
                        Выйти <LogoutOutlined style={{ color: '#fff' }} />
                    </Link>
                </Col>
            </Header>
            <Layout>
                <MediaQuery query={desktopSize}>
                    <Sider width={200} style={{ background: colorBgContainer }}>
                        <Menu
                            mode='inline'
                            defaultSelectedKeys={['/dashboard/profile']}
                            defaultOpenKeys={['/dashboard/profile']}
                            activeKey={location.pathname}
                            style={{ height: '100%', borderRight: 0 }}
                            items={menuItems}
                            onSelect={(item) => setRouteActive(item.key)}
                        />
                    </Sider>
                </MediaQuery>

                <Layout className='content' style={{ padding: '24px 24px 24px' }}>
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

                <MediaQuery query={mobileSize}>
                    <div className='mobile-menu'>
                        <TabBar
                            activeKey={location.pathname}
                            onChange={(value) => setRouteActive(value)}
                        >
                            {menuItems.map((item) => (
                                <TabBar.Item key={item.key} icon={item.icon} title={item.label} />
                            ))}
                        </TabBar>
                    </div>
                </MediaQuery>
            </Layout>
        </Layout>
    );
};

export default DashboardLayout;
