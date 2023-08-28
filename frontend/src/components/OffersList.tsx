import React, { useState } from 'react';
import { Button, InputNumber, Modal, Space, Table, Typography } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Offer } from '../api/models';

const data: Offer[] = [
    {
        cfa_image_id: 1,
        price: 100,
        count: 23,
        id: 1,
        seller_id: 1,
    },
];

const OffersList: React.FC = () => {
    const [open, setOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);

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
            title: 'ID продавца',
            dataIndex: 'seller_id',
            key: 'seller_id',
        },
        {
            title: '',
            key: 'action',
            render: () => {
                return (
                    <Space size='middle'>
                        <Button onClick={buyCfa} size='small'>
                            Купить
                        </Button>
                    </Space>
                );
            },
        },
    ];

    const handleOk = () => {
        setConfirmLoading(true);
        setTimeout(() => {
            setOpen(false);
            setConfirmLoading(false);
        }, 2000);
    };

    const handleCancel = () => {
        console.log('Clicked cancel button');
        setOpen(false);
    };

    const buyCfa = () => {
        setOpen(true);
    };

    const handleCountChange = (count: number | null) => {
        console.log(count);
    };

    return (
        <>
            <Table columns={columns} dataSource={data.map((row) => ({ ...row, key: row.id }))} />

            <Modal
                title='Купить ЦФА'
                open={open}
                onOk={handleOk}
                confirmLoading={confirmLoading}
                onCancel={handleCancel}
                okText='Купить'
                cancelText='Отмена'
            >
                <Typography.Paragraph>Цена лота 100 ₽</Typography.Paragraph>
                <InputNumber
                    style={{ width: '100%' }}
                    placeholder='Введите количество'
                    onChange={handleCountChange}
                />
            </Modal>
        </>
    );
};

export default OffersList;
