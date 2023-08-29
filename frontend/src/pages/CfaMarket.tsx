import { Row, Tabs, TabsProps, Typography } from 'antd';
import CfaList from '../components/CfaList';
import { useEffect, useState } from 'react';
import { useStores } from '../hooks/useStores';
import { CfaImage } from '../api/models';
import { observer } from 'mobx-react-lite';

const CfaMarket = observer(() => {
    const { rootStore } = useStores();
    const [cfas, setCfas] = useState<CfaImage[]>([]);

    useEffect(() => {
        async function fetchCfas() {
            const cfas = await rootStore.getCfaImages();
            setCfas(cfas);
        }
        fetchCfas();
    }, [rootStore, rootStore.trigger]);

    const items: TabsProps['items'] = [
        {
            key: '1',
            label: 'Все ЦФА',
            children: <CfaList cfas={cfas} />,
        },
    ];

    return (
        <>
            <Row>
                <Typography.Title level={2}>Витрина ЦФА</Typography.Title>
            </Row>

            <Row>
                <Tabs style={{ width: '100%' }} defaultActiveKey='1' items={items} />
            </Row>
        </>
    );
});

export default CfaMarket;
