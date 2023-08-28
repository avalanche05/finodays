import { Button, Row, Tabs, TabsProps, Typography } from 'antd';
import CfaList from '../components/CfaList';

const CfaMarket = () => {
    const onChange = (key: string) => {
        console.log(key);
    };

    const items: TabsProps['items'] = [
        {
            key: '1',
            label: 'Все ЦФА',
            children: <CfaList />,
        },
        {
            key: '2',
            label: 'Мои ЦФА',
            children: 'Мои ЦФА',
        },
    ];

    return (
        <>
            <Row>
                <Typography.Title level={2}>Витрина ЦФА</Typography.Title>
            </Row>

            <Row>
                <Tabs
                    style={{ width: '100%' }}
                    tabBarExtraContent={<Button>Продать ЦФА</Button>}
                    defaultActiveKey='1'
                    items={items}
                    onChange={onChange}
                />
            </Row>
        </>
    );
};

export default CfaMarket;
