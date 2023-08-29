import { useState } from 'react';
import { Button, Modal, Space, Table, message } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Deal, DealItem } from '../api/models';
import { useStores } from '../hooks/useStores';

type Props = {
    deals: Deal[];
};

const OwnDealsList = ({ deals }: Props) => {
    const { rootStore } = useStores();
    const [messageApi, contextHolder] = message.useMessage();
    const [open, setOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [selectedDeal, setSelectedDeal] = useState<Deal>(deals[0]);

    const columns: ColumnsType<Deal> = [
        {
            title: 'Пользователь',
            dataIndex: 'user',
            key: 'user',
        },
        {
            title: 'Мои ЦФА',
            dataIndex: 'myCfa',
            key: 'myCfa',
            render: (dealItems: DealItem[]) =>
                dealItems.map((dealItem, index) => (
                    <div key={index}>
                        {dealItem.cfa_image.title} ({dealItem.count})
                    </div>
                )),
        },
        {
            title: 'Цфа пользователя',
            dataIndex: 'userCfa',
            key: 'userCfa',
            render: (dealItems: DealItem[]) =>
                dealItems.map((dealItem, index) => (
                    <div key={index}>
                        {dealItem.cfa_image.title} ({dealItem.count})
                    </div>
                )),
        },
        {
            title: '',
            key: 'action',
            render: (row) => {
                return (
                    <Space size='middle'>
                        <Button danger type='text' onClick={() => deleteDeal(row)} size='small'>
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
            .cancelDeal(selectedDeal.id)
            .then(() => {
                messageApi.success('Сделка отменена');
                rootStore.setTrigger();
            })
            .catch(() => {
                messageApi.error('Ошибка отмены сделки');
            })
            .finally(() => {
                setConfirmLoading(false);
                setOpen(false);
            });
    };

    const handleCancel = () => {
        setOpen(false);
    };

    const deleteDeal = (deal: Deal) => {
        setSelectedDeal(deal);
        setOpen(true);
    };

    return (
        <>
            {contextHolder}
            <Table
                columns={columns}
                dataSource={
                    deals
                        ? deals.map((row) => ({
                              ...row,
                              key: row.id,
                              user: row.host.name,
                              myCfa: row.initiator_items,
                              userCfa: row.host_items,
                          }))
                        : []
                }
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

export default OwnDealsList;
