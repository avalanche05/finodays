import { useState } from 'react';
import {
    Button,
    ConfigProvider,
    Empty,
    InputNumber,
    Modal,
    Space,
    Table,
    Typography,
    message,
} from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Offer } from '../api/models';
import { useStores } from '../hooks/useStores';

type Props = {
    offers: Offer[];
};

const OffersList = ({ offers }: Props) => {
    const { rootStore } = useStores();
    const [messageApi, contextHolder] = message.useMessage();
    const [open, setOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [selectedOffer, setSelectedOffer] = useState<Offer>(offers[0]);
    const [count, setCount] = useState<number>(0);

    const columns: ColumnsType<Offer> = [
        {
            title: 'Стоимость',
            dataIndex: 'price',
            key: 'price',
            render: (text) => <span>{text} ₽</span>,
        },
        {
            title: 'Количество',
            dataIndex: 'count',
            key: 'count',
        },
        {
            title: 'Продавец',
            dataIndex: 'sellerName',
            key: 'sellerName',
        },
        {
            title: '',
            key: 'action',
            render: (row) => {
                return (
                    <Space size='middle'>
                        <Button onClick={() => buyCfa(row)} size='small'>
                            Купить
                        </Button>
                    </Space>
                );
            },
        },
    ];

    const handleOk = () => {
        setConfirmLoading(true);

        rootStore
            .buyOffer({ ...selectedOffer, count })
            .then(() => {
                messageApi.success('ЦФА куплен');
                rootStore.setTrigger();
            })
            .catch((error) => {
                messageApi.error(error.response.data);
            })
            .finally(() => {
                setConfirmLoading(false);
                setOpen(false);
            });
    };

    const handleCancel = () => {
        console.log('Clicked cancel button');
        setOpen(false);
    };

    const buyCfa = (offer: Offer) => {
        setSelectedOffer(offer);
        setOpen(true);
    };

    return (
        <>
            {contextHolder}
            <ConfigProvider renderEmpty={() => <Empty description='Нет еще ни одного оффера' />}>
                <Table
                    columns={columns}
                    dataSource={offers.map((row) => ({
                        ...row,
                        key: row.id,
                        sellerName: row.seller.name,
                    }))}
                />
            </ConfigProvider>

            <Modal
                title='Купить ЦФА'
                open={open}
                onOk={handleOk}
                confirmLoading={confirmLoading}
                onCancel={handleCancel}
                okText='Купить'
                cancelText='Отмена'
            >
                <Typography.Paragraph>Цена лота {selectedOffer?.price} ₽</Typography.Paragraph>
                <InputNumber
                    onChange={(value) => {
                        if (value) {
                            setCount(parseInt(value.toString()));
                        } else {
                            setCount(0);
                        }
                    }}
                    style={{ width: '100%' }}
                    placeholder='Введите количество'
                />
            </Modal>
        </>
    );
};

export default OffersList;
