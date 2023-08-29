import { Row, Tabs, TabsProps } from 'antd';
import { Deal } from '../api/models';
import { useEffect, useState } from 'react';
import { useStores } from '../hooks/useStores';
import { observer } from 'mobx-react-lite';
import OwnDealsList from './DealsList';

const OwnDealsTabs = observer(() => {
    const { rootStore } = useStores();
    const [outgoingDeals, setOutgoingDeals] = useState<Deal[]>([]);
    const [incomingDeals, setIncomingDeals] = useState<Deal[]>([]);

    const items: TabsProps['items'] = [
        {
            key: '1',
            label: 'Исходящие сделки',
            children: <OwnDealsList deals={outgoingDeals} />,
        },
        {
            key: '2',
            label: 'Входящие сделки',
            children: <OwnDealsList deals={incomingDeals} />,
        },
    ];

    useEffect(() => {
        async function fetchDeals() {
            const outgoingDeals = await rootStore.getOutgoingDeals();
            const incomingDeals = await rootStore.getIncomingDeals();

            setOutgoingDeals(outgoingDeals);
            setIncomingDeals(incomingDeals);
        }
        fetchDeals();
    }, [rootStore, rootStore.trigger]);

    return (
        <>
            <Row>
                <Tabs style={{ width: '100%' }} defaultActiveKey='1' items={items} />
            </Row>
        </>
    );
});

export default OwnDealsTabs;
