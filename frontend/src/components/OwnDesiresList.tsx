import { useState } from 'react';
import { Button, Modal, Space, Table, message } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Desire } from '../api/models';
import { useStores } from '../hooks/useStores';

type Props = {
    desires: Desire[];
};

const OwnDesiresList = ({ desires }: Props) => {
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
            <Table
                columns={columns}
                dataSource={desires.map((row) => ({
                    ...row,
                    key: row.id,
                    cfaImageTitle: row.cfa_image.title,
                }))}
            />

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
