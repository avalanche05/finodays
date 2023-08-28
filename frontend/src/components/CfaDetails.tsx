import { Row, Tabs, TabsProps, Tag, Typography } from 'antd';
import { CfaImage, Offer } from '../api/models';
import OffersList from './OffersList';
import TokensList from './TokensList';
import { useEffect, useState } from 'react';
import { useStores } from '../hooks/useStores';

type Props = {
    cfaImage: CfaImage;
};

const CfaDetails = ({ cfaImage }: Props) => {
    const { rootStore } = useStores();
    const [offers, setOffers] = useState<Offer[]>([]);

    const items: TabsProps['items'] = [
        {
            key: '1',
            label: 'Заявки на продажу',
            children: <OffersList offers={offers} />,
        },
        {
            key: '2',
            label: (
                <>
                    Заявки на покупку <Tag color='warning'>WIP</Tag>
                </>
            ),
            children: 'Заявки на покупку',
            disabled: true,
        },
        {
            key: '3',
            label: (
                <>
                    Заявки на обмен <Tag color='warning'>WIP</Tag>
                </>
            ),
            children: 'Заявки на обмен',
            disabled: true,
        },
    ];

    useEffect(() => {
        async function fetchOffers() {
            const offers = await rootStore.getOffersByCfaImage(cfaImage.id);
            setOffers(offers);
        }
        fetchOffers();
    }, [rootStore, cfaImage]);

    return (
        <>
            <Row>
                <Typography.Title level={2}>{cfaImage.title}</Typography.Title>
            </Row>

            <Row>
                <Typography.Paragraph>{cfaImage.description}</Typography.Paragraph>
            </Row>

            <Row>
                <Tabs style={{ width: '100%' }} defaultActiveKey='1' items={items} />
            </Row>

            <Row>
                <Typography.Title level={3}>Список токенов</Typography.Title>
            </Row>
            <Row>
                <TokensList />
            </Row>
        </>
    );
};

export default CfaDetails;
