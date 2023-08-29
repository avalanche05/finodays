import { useState } from 'react';
import { Button, InputNumber, Modal, Space, Table, message } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { Desire } from '../api/models';
import { useStores } from '../hooks/useStores';

type Props = {
    desires: Desire[];
};

const DesiresList = ({ desires }: Props) => {
    const { rootStore } = useStores();
    const [messageApi, contextHolder] = message.useMessage();
    const [open, setOpen] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [selectedDesire, setSelectedDesire] = useState<Desire>(desires[0]);
    const [count, setCount] = useState<number>(0);

    const columns: ColumnsType<Desire> = [
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
            title: 'Покупатель',
            dataIndex: 'buyerName',
            key: 'buyerName',
        },
        {
            title: '',
            key: 'action',
            render: (row) => {
                return (
                    <Space size='middle'>
                        <Button onClick={() => buyCfa(row)} size='small'>
                            Продать
                        </Button>
                    </Space>
                );
            },
        },
    ];

    const handleOk = () => {
        setConfirmLoading(true);

        rootStore
            .sellDesire(selectedDesire.id, count)
            .then(() => {
                messageApi.success('ЦФА продан');
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
        setOpen(false);
    };

    const buyCfa = (desire: Desire) => {
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
                    buyerName: row.buyer?.name,
                }))}
            />

            <Modal
                title='Продать ЦФА'
                open={open}
                onOk={handleOk}
                confirmLoading={confirmLoading}
                onCancel={handleCancel}
                okText='Продать'
                cancelText='Отмена'
            >
                <InputNumber
                    onChange={(value) => {
                        if (value) {
                            setCount(parseInt(value.toString()));
                        } else {
                            setCount(0);
                        }
                    }}
                    style={{ width: '100%' }}
                    placeholder='Введите количество цфа для продажи'
                />
            </Modal>
        </>
    );
};

export default DesiresList;
