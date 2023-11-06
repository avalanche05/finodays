import {
    Button,
    Col,
    Form,
    InputNumber,
    List,
    Row,
    Tour,
    TourProps,
    Typography,
    message,
} from 'antd';
import { OwnCfaImage } from '../api/models';
import { useStores } from '../hooks/useStores';
import { useRef, useState } from 'react';
import { valueType } from 'antd/es/statistic/utils';
import PricePlot from './PricePlot';

type Props = {
    ownCfaImage: OwnCfaImage;
};

const OwnCfaDetails = ({ ownCfaImage }: Props) => {
    const { rootStore } = useStores();
    const [messageApi, contextHolder] = message.useMessage();
    const [form] = Form.useForm();
    const [volume, setVolume] = useState<number>(0);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const [tourOpen, setTourOpen] = useState<boolean>(false);
    const refPriceSetter = useRef(null);
    const refPricePlot = useRef(null);
    const refTokens = useRef(null);

    const onFinish = (form: { count: number; price: number }) => {
        setIsLoading(true);

        rootStore
            .createOffer(ownCfaImage.cfa_image.id, form.count, form.price)
            .then(() => {
                messageApi.success('Оффер успешно создан');
                rootStore.setTrigger();
            })
            .catch(() => {
                messageApi.error('Ошибка создания оффера');
            })
            .finally(() => setIsLoading(false));
    };

    const handlePriceChange = (price: valueType | null) => {
        const count = form.getFieldValue('count');

        if (price && count) {
            setVolume(+price * count);
        }
    };

    const handleCountChange = (count: valueType | null) => {
        const price = form.getFieldValue('price');

        if (price && count) {
            setVolume(price * +count);
        }
    };

    const steps: TourProps['steps'] = [
        {
            title: 'Создание заявки на продажу',
            description:
                'Чтобы создать заявку на продажу, нужно выбрать количество токенов и цену за токен. После этого нажмите кнопку "Создать оффер". В поле "Объем выпуска" отображается сумма, которую вы получите за продажу всех токенов.',
            target: () => refPriceSetter.current,
            nextButtonProps: { children: 'Далее' },
            className: 'tour-step',
        },
        {
            title: 'График цены',
            description:
                'На графике представлена история цены ЦФА. Чтобы увидеть подробную информацию о цене в определенный момент времени, наведите курсор на нужную точку.',
            target: () => refPricePlot.current,
            nextButtonProps: { children: 'Далее' },
            prevButtonProps: { children: 'Назад' },
            className: 'tour-step',
        },
        {
            title: 'Список токенов',
            description: 'В этом списке представлены все токены, которыми вы владеете.',
            target: () => refTokens.current,
            className: 'tour-step',
            prevButtonProps: { children: 'Назад' },
            nextButtonProps: { children: 'Завершить' },
        },
    ];

    return (
        <>
            {contextHolder}
            <Row justify={'space-between'} align={'middle'} style={{ marginBottom: 16 }}>
                <Typography.Title style={{ marginBottom: 0 }} level={2}>
                    {ownCfaImage.cfa_image.title}
                </Typography.Title>

                <Button type='default' onClick={() => setTourOpen(true)}>
                    Обучение
                </Button>
            </Row>

            <Row>
                <Typography.Paragraph>{ownCfaImage.cfa_image.description}</Typography.Paragraph>
            </Row>

            <Row ref={refPriceSetter}>
                <Form
                    onFinish={onFinish}
                    layout={'vertical'}
                    form={form}
                    style={{ width: '100%', maxWidth: 800 }}
                >
                    <Row gutter={[8, 24]}>
                        <Col span={8}>
                            <Form.Item
                                name={'price'}
                                rules={[
                                    {
                                        required: true,
                                        message: 'Пожалуйста, введите цену ЦФА',
                                    },
                                ]}
                                label='Цена размещения'
                            >
                                <InputNumber
                                    style={{ width: '100%' }}
                                    placeholder='1000 ₽'
                                    formatter={(value) =>
                                        ` ${value} ₽`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
                                    }
                                    onChange={(e) => handlePriceChange(e)}
                                    min={0}
                                />
                            </Form.Item>
                        </Col>

                        <Col span={8}>
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
                                    max={ownCfaImage.cfa_image.count}
                                    onChange={(e) => handleCountChange(e)}
                                    style={{ width: '100%' }}
                                    placeholder='100'
                                    min={0}
                                />
                            </Form.Item>
                        </Col>

                        <Col span={8}>
                            <Form.Item label='Объем выпуска'>
                                <InputNumber
                                    disabled
                                    value={volume}
                                    style={{ width: '100%' }}
                                    placeholder='100000 ₽'
                                    formatter={(value) => `${value} ₽`}
                                    min={0}
                                />
                            </Form.Item>
                        </Col>
                    </Row>

                    <Row>
                        <Form.Item>
                            <Button loading={isLoading} type='primary' htmlType='submit'>
                                Создать оффер
                            </Button>
                        </Form.Item>
                    </Row>
                </Form>
            </Row>

            <div ref={refPricePlot}>
                <Row>
                    <Typography.Title level={3}>История цены</Typography.Title>
                </Row>

                <Row>
                    <PricePlot
                        cfaImageId={ownCfaImage.cfa_image.id}
                        cfaTitle={ownCfaImage.cfa_image.title}
                    />
                </Row>
            </div>

            <div ref={refTokens}>
                <Row>
                    <Typography.Title level={3}>Список токенов</Typography.Title>
                </Row>

                <Row>
                    <List
                        size='small'
                        bordered
                        dataSource={ownCfaImage.tokens.slice(0, 10)}
                        renderItem={(item) => <List.Item>{item.slice(0, 30)}</List.Item>}
                    />
                </Row>
            </div>

            <Tour open={tourOpen} onClose={() => setTourOpen(false)} steps={steps} />
        </>
    );
};

export default OwnCfaDetails;
