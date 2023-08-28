import { Button, Col, Form, InputNumber, List, Row, Typography, message } from 'antd';
import { OwnCfaImage } from '../api/models';
import { useStores } from '../hooks/useStores';
import { Dispatch, SetStateAction, useState } from 'react';
import { valueType } from 'antd/es/statistic/utils';

type Props = {
    ownCfaImage: OwnCfaImage;
    trigger: Dispatch<SetStateAction<boolean>>;
    triggerValue: boolean;
};

const OwnCfaDetails = ({ ownCfaImage, trigger, triggerValue }: Props) => {
    const { rootStore } = useStores();
    const [messageApi, contextHolder] = message.useMessage();
    const [form] = Form.useForm();
    const [volume, setVolume] = useState<number>(0);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    const onFinish = (form: { count: number; price: number }) => {
        setIsLoading(true);

        rootStore
            .createOffer(ownCfaImage.cfa_image.id, form.count, form.price)
            .then(() => {
                messageApi.success('Оффер успешно создан');
                trigger(!triggerValue);
            })
            .catch(() => {
                messageApi.error('Ошибка создания оффера');
            })
            .finally(() => setIsLoading(false));

        console.log('Success:', form);
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

    return (
        <>
            {contextHolder}
            <Row>
                <Typography.Title level={2}>{ownCfaImage.cfa_image.title}</Typography.Title>
            </Row>

            <Row>
                <Typography.Paragraph>{ownCfaImage.cfa_image.description}</Typography.Paragraph>
            </Row>

            <Row>
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
                                        message: 'Пожалуйста, введите количество ЦФА',
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

            <Row>
                <Typography.Title level={3}>Список токенов</Typography.Title>
            </Row>
            <Row>
                <List
                    size='small'
                    bordered
                    dataSource={ownCfaImage.tokens.slice(0, 10)}
                    renderItem={(item) => <List.Item>{item}</List.Item>}
                />
            </Row>
        </>
    );
};

export default OwnCfaDetails;
