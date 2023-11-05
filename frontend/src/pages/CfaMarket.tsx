import { Row, Tabs, TabsProps, Typography } from 'antd';
import CfaList from '../components/CfaList';
import { useEffect, useState } from 'react';
import { useStores } from '../hooks/useStores';
import { CfaImage } from '../api/models';
import { observer } from 'mobx-react-lite';

const CfaMarket = observer(() => {
    const { rootStore } = useStores();
    const [cfas, setCfas] = useState<CfaImage[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    useEffect(() => {
        async function fetchCfas() {
            setLoading(true);

            const cfas = await rootStore.getCfaImages();
            setCfas(cfas);
            setLoading(false);
        }
        fetchCfas();
    }, [rootStore, rootStore.trigger]);

    const items: TabsProps['items'] = [
        {
            key: '1',
            label: 'Все ЦФА',
            children: <CfaList cfas={cfas} loading={loading} />,
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
