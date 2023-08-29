import { useState } from 'react';
import { Button, Modal, Space, Table, message } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Offer } from '../api/models';
import { useStores } from '../hooks/useStores';

type Props = {
    offers: Offer[];
};

const OwnOffersList = ({ offers }: Props) => {
    const { rootStore } = useStores();
    const [messageApi, contextHolder] = message.useMessage();
    const [open, setOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [selectedOffer, setSelectedOffer] = useState<Offer>(offers[0]);

    const columns: ColumnsType<Offer> = [
        {
            title: 'Название ЦФА',
            dataIndex: 'cfaImageTitle',
            key: 'cfaImageTitle',
        },
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
            title: '',
            key: 'action',
            render: (row) => {
                return (
                    <Space size='middle'>
                        <Button danger type='text' onClick={() => deleteOffer(row)} size='small'>
                            Удалить
                        </Button>
                    </Space>
                );
            },
        },
    ];

    const handleOk = () => {
        setConfirmLoading(true);

        rootStore
            .deleteOffer(selectedOffer.id)
            .then(() => {
                messageApi.success('Оффер удален');
                rootStore.setTrigger();
            })
            .catch(() => {
                messageApi.error('Ошибка удаления оффера');
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

    const deleteOffer = (offer: Offer) => {
        setSelectedOffer(offer);
        setOpen(true);
    };

    return (
        <>
            {contextHolder}
            <Table
                columns={columns}
                dataSource={offers.map((row) => ({
                    ...row,
                    key: row.id,
                    sellerName: row.seller.name,
                    cfaImageTitle: row.cfa_image.title,
                }))}
            />

            <Modal
                title='Подтверждение удаления оффера'
                open={open}
                onOk={handleOk}
                confirmLoading={confirmLoading}
                onCancel={handleCancel}
                okText='Удалить'
                cancelText='Отмена'
            ></Modal>
        </>
    );
};

export default OwnOffersList;
