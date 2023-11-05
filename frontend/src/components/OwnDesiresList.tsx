import { useState } from 'react';
import { Button, ConfigProvider, Empty, Modal, Space, Table, message } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Desire } from '../api/models';
import { useStores } from '../hooks/useStores';

type Props = {
    desires: Desire[];
    loading: boolean;
};

const OwnDesiresList = ({ desires, loading }: Props) => {
    const { rootStore } = useStores();
    const [messageApi, contextHolder] = message.useMessage();
    const [open, setOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [selectedDesire, setSelectedDesire] = useState<Desire>(desires[0]);

    const columns: ColumnsType<Desire> = [
        {
            title: 'Название ЦФА',
            dataIndex: 'cfaImageTitle',
            key: 'cfaImageTitle',
        },
        {
            title: 'Желаемая стоимость',
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
                        <Button danger type='text' onClick={() => deleteDesire(row)} size='small'>
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
            .deleteDesire(selectedDesire.id)
            .then(() => {
                messageApi.success('Заявка на покупку удалена');
                rootStore.setTrigger();
            })
            .catch(() => {
                messageApi.error('Ошибка удаления заявки на покупку');
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

    const deleteDesire = (desire: Desire) => {
        setSelectedDesire(desire);
        setOpen(true);
    };

    return (
        <>
            {contextHolder}
            <ConfigProvider renderEmpty={() => <Empty description='Нет еще ни одной заявки' />}>
                <Table
                    columns={columns}
                    dataSource={desires.map((row) => ({
                        ...row,
                        key: row.id,
                        cfaImageTitle: row.cfa_image.title,
                    }))}
                    loading={loading}
                />
            </ConfigProvider>

            <Modal
                title='Подтверждение удаления заявки на покупку'
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

export default OwnDesiresList;
