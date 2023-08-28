import {
    Button,
    Checkbox,
    Col,
    DatePicker,
    Form,
    Input,
    InputNumber,
    Row,
    Typography,
    message,
} from 'antd';
import TextArea from 'antd/es/input/TextArea';
import { valueType } from 'antd/es/statistic/utils';
import { useState } from 'react';
import { CreateCfaForm } from '../models/CreateCfaForm';
import { CheckboxChangeEvent } from 'antd/es/checkbox';
import { useStores } from '../hooks/useStores';

const CreateCfa = () => {
    const [messageApi, contextHolder] = message.useMessage();
    const [isInitialOfferActive, setIsInitialOfferActive] = useState<boolean>(false);
    const [form] = Form.useForm();
    const [volume, setVolume] = useState<number>(0);
    const { rootStore } = useStores();
    const [isCfaCreating, setIsCfaCreating] = useState<boolean>(false);

    const onFinish = (createCfaForm: CreateCfaForm) => {
        setIsCfaCreating(true);

        rootStore
            .createCfa(createCfaForm)
            .then(() => {
                messageApi.success('ЦФА успешно создана');
            })
            .catch(() => {
                messageApi.error('Ошибка создания ЦФА');
            })
            .finally(() => setIsCfaCreating(false));

        console.log('Success:', createCfaForm);
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
                <Typography.Title level={2}>Новая заявка на выпуск ЦФА</Typography.Title>
            </Row>
            <Row>
                <Form
                    onFinish={onFinish}
                    layout={'vertical'}
                    form={form}
                    style={{ width: '100%', maxWidth: 800 }}
                >
                    <Row>
                        <Col span={12}>
                            <Form.Item
                                name={'title'}
                                rules={[
                                    {
                                        required: true,
                                        message: 'Пожалуйста, введите имя название ЦФА',
                                    },
                                ]}
                                label='Название ЦФА'
                            >
                                <Input placeholder='Например: ООО "Полет" - денежное требование' />
                            </Form.Item>
                        </Col>
                    </Row>
                    <Row>
                        <Col span={24}>
                            <Form.Item
                                name={'description'}
                                rules={[
                                    {
                                        required: true,
                                        message: 'Пожалуйста, введите Описание',
                                    },
                                ]}
                                label='Описание ЦФА'
                            >
                                <TextArea placeholder='Описание ЦФА' />
                            </Form.Item>
                        </Col>
                    </Row>

                    <Row>
                        <Form.Item name='isInitialOfferActive' valuePropName='checked'>
                            <Checkbox
                                onChange={(e: CheckboxChangeEvent) => {
                                    setIsInitialOfferActive(e.target.checked);
                                }}
                            >
                                Активировать заявку на продажу
                            </Checkbox>
                        </Form.Item>
                    </Row>

                    <Row gutter={[8, 24]}>
                        {isInitialOfferActive && (
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
                        )}

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
                                    onChange={(e) => handleCountChange(e)}
                                    style={{ width: '100%' }}
                                    placeholder='100'
                                />
                            </Form.Item>
                        </Col>
                        {isInitialOfferActive && (
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
                        )}
                    </Row>

                    <Row>
                        <Typography.Title level={4}>Условия выпуска</Typography.Title>
                    </Row>

                    <Row gutter={[8, 24]}>
                        <Col span={12}>
                            <Form.Item label='Дата выпуска'>
                                <DatePicker style={{ width: '100%' }} placeholder='Выберите дату' />
                            </Form.Item>
                        </Col>
                        <Col span={12}>
                            <Form.Item label='Дата погашения'>
                                <DatePicker style={{ width: '100%' }} placeholder='Выберите дату' />
                            </Form.Item>
                        </Col>
                    </Row>

                    <Row>
                        <Form.Item>
                            <Button loading={isCfaCreating} type='primary' htmlType='submit'>
                                Подать заявку
                            </Button>
                        </Form.Item>
                    </Row>
                </Form>
            </Row>
        </>
    );
};

export default CreateCfa;
