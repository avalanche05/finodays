import { useState } from 'react';
import { Avatar, Button, Drawer, Space, Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { UserOutlined } from '@ant-design/icons';
import CfaDetails from './CfaDetails';
import { CfaImage } from '../api/models';

type Props = {
    cfas: CfaImage[];
};

const CfaList = ({ cfas }: Props) => {
    const [isDrawerOpen, setIsDrawerOpen] = useState(false);
    const [selectedRowId, setSelectedRowId] = useState<number>(0);

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
            render: (row) => {
                return (
                    <Space size='middle'>
                        <Button onClick={() => showDrawer(row.id)} size='small'>
                            Предложения
                        </Button>
                    </Space>
                );
            },
        },
    ];

    const showDrawer = (rowId: number) => {
        setSelectedRowId(rowId - 1);
        setIsDrawerOpen(true);
    };

    const onClose = () => {
        setIsDrawerOpen(false);
    };

    return (
        <>
            <Table
                columns={columns}
                dataSource={cfas.map((row) => ({ ...row, key: row.id, issuer: row.user.name }))}
            />

            <Drawer
                title='Подробнее про ЦФА'
                placement='right'
                size={'large'}
                onClose={onClose}
                open={isDrawerOpen}
            >
                <CfaDetails cfaImage={cfas[selectedRowId]} />
            </Drawer>
        </>
    );
};

export default CfaList;
