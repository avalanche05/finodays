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
    Tour,
    TourProps,
    Typography,
    message,
} from 'antd';
import { CfaImage, Desire, Offer } from '../api/models';
import OffersList from './OffersList';
import { useEffect, useRef, useState } from 'react';
import { useStores } from '../hooks/useStores';
import DesiresList from './DesiresList';
import { observer } from 'mobx-react-lite';
import PricePlot from './PricePlot';
import { IBuyAdvice } from '../api/models/IBuyAdvice';

type Props = {
    cfaImage: CfaImage;
};

const CfaDetails = observer(({ cfaImage }: Props) => {
    const [messageApi, contextHolder] = message.useMessage();
    const { rootStore } = useStores();
    const [offers, setOffers] = useState<Offer[]>([]);
    const [desires, setDesires] = useState<Desire[]>([]);
    const [buyAdvice, setBuyAdvice] = useState<IBuyAdvice | null>(null);
    const [isDesireCreating, setIsDesireCreating] = useState<boolean>(false);
    const [open, setOpen] = useState(false);
    const [form] = Form.useForm();

    const [tourOpen, setTourOpen] = useState<boolean>(false);
    const refOffers = useRef(null);
    const refDesires = useRef(null);
    const refCreateDesire = useRef(null);
    const refPricePlot = useRef(null);

    const items: TabsProps['items'] = [
        {
            key: '1',
            label: <div ref={refOffers}>Заявки на продажу</div>,
            children: <OffersList offers={offers} />,
        },
        {
            key: '2',
            label: <div ref={refDesires}>Заявки на покупку</div>,
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
            const offers = await rootStore
                .getOffersByCfaImage(cfaImage.id)
                .catch((error) => console.log(error));
            const desires = await rootStore
                .getDesiresByCfaImage(cfaImage.id)
                .catch((error) => console.log(error));
            const fetchedBuyAdvice = await rootStore.getBuyAdvice(cfaImage.id);

            setOffers(offers);
            setDesires(desires);
            setBuyAdvice(fetchedBuyAdvice);
        }
        fetchOffers();
    }, [rootStore, cfaImage, rootStore.trigger]);

    const handleOk = () => {
        form.validateFields();

        const desire = {
            ...form.getFieldsValue(),
            cfa_image: cfaImage,
        };

        if (desire && desire.count && desire.price) {
            setIsDesireCreating(true);

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
        setOpen(false);
    };

    const createDesire = () => {
        setOpen(true);
    };

    const steps: TourProps['steps'] = [
        {
            title: 'Предложения на продажу',
            description:
                'В этом списке представлены все заявки на продажу ЦФА. Чтобы купить ЦФА, нажмите кнопку "Купить".',
            target: () => refOffers.current,
            nextButtonProps: { children: 'Далее' },
            className: 'tour-step',
        },
        {
            title: 'Предложения на покупку',
            description:
                'В этом списке представлены все заявки на покупку ЦФА. Чтобы продать ЦФА, нажмите кнопку "Продать".',
            target: () => refDesires.current,
            nextButtonProps: { children: 'Далее' },
            prevButtonProps: { children: 'Назад' },
            className: 'tour-step',
        },
        {
            title: 'Создать заяку на покупку',
            description:
                'Чтобы создать заявку на покупку, нажмите кнопку "Создать заявку" и введите цену и количество ЦФА.',
            target: () => refCreateDesire.current,
            nextButtonProps: { children: 'Далее' },
            prevButtonProps: { children: 'Назад' },
            className: 'tour-step',
        },
        {
            title: 'График цены',
            description:
                'На графике представлена история цены ЦФА. Чтобы увидеть подробную информацию о цене в определенный момент времени, наведите курсор на нужную точку.',
            target: () => refPricePlot.current,
            prevButtonProps: { children: 'Назад' },
            nextButtonProps: { children: 'Завершить' },
            className: 'tour-step',
        },
    ];

    return (
        <>
            {contextHolder}
            <div style={{ paddingBottom: 100 }}>
                <Row justify={'space-between'} align={'middle'} style={{ marginBottom: 16 }}>
                    <Typography.Title level={2} style={{ marginBottom: 0 }}>
                        {cfaImage.title}
                    </Typography.Title>

                    <Button type='default' onClick={() => setTourOpen(true)}>
                        Обучение
                    </Button>
                </Row>

                <Row>
                    <Typography.Paragraph>{cfaImage.description}</Typography.Paragraph>
                </Row>

                {buyAdvice && buyAdvice.why && buyAdvice.why.ru && (
                    <Row>
                        <Tag color={buyAdvice.is_buy ? 'success' : 'warning'}>
                            {buyAdvice?.why.ru}
                        </Tag>
                    </Row>
                )}

                <Row>
                    <Tabs
                        style={{ width: '100%' }}
                        defaultActiveKey='1'
                        items={items}
                        tabBarExtraContent={
                            <Button ref={refCreateDesire} onClick={createDesire}>
                                Создать заявку
                            </Button>
                        }
                    />
                </Row>

                <Row>
                    <Typography.Title level={3}>История цены</Typography.Title>
                </Row>

                <Row>
                    <Typography.Paragraph>
                        Историй цены ЦФА на основе предыдущих сделок. По горизонтали - 3 последних
                        дня, по вертикали - цена в рублях.
                    </Typography.Paragraph>
                </Row>

                <Row ref={refPricePlot}>
                    <PricePlot cfaImageId={cfaImage.id} cfaTitle={cfaImage.title} />
                </Row>
            </div>

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
                    кто-то создаст оффер с ЦФА по вашей цене, он будет автоматически исполнен.
                </Typography.Paragraph>

                <Form layout={'vertical'} form={form} style={{ width: '100%', maxWidth: 800 }}>
                    <Row gutter={[8, 24]}>
                        <Col span={12}>
                            <Form.Item
                                name={'price'}
                                rules={[
                                    {
                                        required: true,
                                        message: 'Пожалуйста, введите цену ЦФА',
                                    },
                                ]}
                                label='Цена покупки'
                            >
                                <InputNumber
                                    min={0}
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
                                <InputNumber
                                    min={0}
                                    max={1000}
                                    style={{ width: '100%' }}
                                    placeholder='100'
                                />
                            </Form.Item>
                        </Col>
                    </Row>
                </Form>
            </Modal>

            <Tour open={tourOpen} onClose={() => setTourOpen(false)} steps={steps} />
        </>
    );
});

export default CfaDetails;
