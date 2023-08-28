import React, { useState } from 'react';
import { Avatar, Button, Drawer, Space, Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { UserOutlined } from '@ant-design/icons';
import CfaDetails from './CfaDetails';
import { CfaImage } from '../api/models';

const data: CfaImage[] = [
    {
        title: 'John Brown',
        issuer: 'АО Ромашка',
        count: 23,
        description: 'desc',
        id: 1,
    },
];

const CfaList: React.FC = () => {
    const [open, setOpen] = useState(false);

    const columns: ColumnsType<CfaImage> = [
        {
            title: 'Наименование',
            dataIndex: 'title',
            key: 'title',
            render: (text) => <a>{text}</a>,
        },
        {
            title: 'Эмитент',
            dataIndex: 'issuer',
            key: 'issuer',
            render: (text) => {
                return (
                    <div>
                        <Avatar style={{ backgroundColor: `#9bcff9` }} icon={<UserOutlined />} />

                        <span style={{ marginLeft: 10 }}>{text}</span>
                    </div>
                );
            },
        },
        {
            title: 'Количество',
            dataIndex: 'count',
            key: 'count',
        },
        {
            title: '',
            key: 'action',
            render: () => {
                return (
                    <Space size='middle'>
                        <Button onClick={showDrawer} size='small'>
                            Предложения
                        </Button>
                    </Space>
                );
            },
        },
    ];

    const showDrawer = () => {
        setOpen(true);
    };

    const onClose = () => {
        setOpen(false);
    };

    return (
        <>
            <Table columns={columns} dataSource={data.map((row) => ({ ...row, key: row.id }))} />

            <Drawer
                title='Подробнее про ЦФА'
                placement='right'
                size={'large'}
                onClose={onClose}
                open={open}
            >
                <CfaDetails cfaImage={data[0]} />
            </Drawer>
        </>
    );
};

export default CfaList;
