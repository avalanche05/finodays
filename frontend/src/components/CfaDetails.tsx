import {
    Button,
    Col,
    Form,
    InputNumber,
    Modal,
    Row,
    Tabs,
    TabsProps,
    Tag,
    Typography,
    message,
} from 'antd';
import { CfaImage, Desire, Offer } from '../api/models';
import OffersList from './OffersList';
import { useEffect, useState } from 'react';
import { useStores } from '../hooks/useStores';
import DesiresList from './DesiresList';
import { observer } from 'mobx-react-lite';

type Props = {
    cfaImage: CfaImage;
};

const CfaDetails = observer(({ cfaImage }: Props) => {
    const [messageApi, contextHolder] = message.useMessage();
    const { rootStore } = useStores();
    const [offers, setOffers] = useState<Offer[]>([]);
    const [desires, setDesires] = useState<Desire[]>([]);
    const [isDesireCreating, setIsDesireCreating] = useState<boolean>(false);
    const [open, setOpen] = useState(false);
    const [form] = Form.useForm();

    const items: TabsProps['items'] = [
        {
            key: '1',
            label: 'Заявки на продажу',
            children: <OffersList offers={offers} />,
        },
        {
            key: '2',
            label: 'Заявки на покупку',
            children: <DesiresList desires={desires} />,
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
            const desires = await rootStore.getDesiresByCfaImage(cfaImage.id);

            setOffers(offers);
            setDesires(desires);
        }
        fetchOffers();
    }, [rootStore, cfaImage, rootStore.trigger]);

    const handleOk = () => {
        setIsDesireCreating(true);

        const desire = {
            ...form.getFieldsValue(),
            cfa_image: cfaImage,
        };

        if (desire && desire.count && desire.price) {
            rootStore
                .createDesire(desire.cfa_image.id, desire.count, desire.price)
                .then(() => {
                    messageApi.success('Заявка на покупку ЦФА создана');
                    rootStore.setTrigger();
                })
                .catch((error) => {
                    console.log(error);

                    messageApi.error('ошибка создания заявки');
                })
                .finally(() => {
                    setIsDesireCreating(false);
                    setOpen(false);
                });
        }
    };

    const handleCancel = () => {
        console.log('Clicked cancel button');
        setOpen(false);
    };

    const createDesire = () => {
        setOpen(true);
    };

    return (
        <>
            {contextHolder}
            <Row>
                <Typography.Title level={2}>{cfaImage.title}</Typography.Title>
            </Row>

            <Row>
                <Typography.Paragraph>{cfaImage.description}</Typography.Paragraph>
            </Row>

            <Row>
                <Tabs
                    style={{ width: '100%' }}
                    defaultActiveKey='1'
                    items={items}
                    tabBarExtraContent={<Button onClick={createDesire}>Создать заявку</Button>}
                />
            </Row>

            <Modal
                title='Купить ЦФА'
                open={open}
                onOk={handleOk}
                confirmLoading={isDesireCreating}
                onCancel={handleCancel}
                okText='Создать заявку на покупку'
                cancelText='Отмена'
            >
                <Typography.Paragraph>
                    Вы можете задать цену и количество ЦФА, которые вы хотите купить. Как только
                    кто-то создаст оффер с ЦФА по вашей цене, они будут автоматически исполнены.
                </Typography.Paragraph>
                <Form layout={'vertical'} form={form} style={{ width: '100%', maxWidth: 800 }}>
                    <Row gutter={[8, 24]}>
                        <Col span={12}>
                            <Form.Item
                                name={'price'}
                                rules={[
                                    {
                                        required: true,
                                        message: 'Пожалуйста, введите количество ЦФА',
                                    },
                                ]}
                                label='Цена покупки'
                            >
                                <InputNumber
                                    style={{ width: '100%' }}
                                    placeholder='1000 ₽'
                                    formatter={(value) =>
                                        ` ${value} ₽`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
                                    }
                                />
                            </Form.Item>
                        </Col>

                        <Col span={12}>
                            <Form.Item
                                name={'count'}
                                rules={[
                                    {
                                        required: true,
                                        message: 'Пожалуйста, введите количество ЦФА',
                                    },
                                ]}
                                label='Количество ЦФА'
                            >
                                <InputNumber style={{ width: '100%' }} placeholder='100' />
                            </Form.Item>
                        </Col>
                    </Row>
                </Form>
            </Modal>
        </>
    );
});

export default CfaDetails;
