import { useState } from 'react';
import { Button, Drawer, Space, Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import CfaDetails from './CfaDetails';
import { CfaImage } from '../api/models';

type Props = {
    cfas: CfaImage[];
    loading: boolean;
};

const CfaList = ({ cfas, loading }: Props) => {
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
                return <span>{text}</span>;
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
        setSelectedRowId(rowId);
        setIsDrawerOpen(true);
    };

    const onClose = () => {
        setIsDrawerOpen(false);
    };

    const getCfaImageById = (id: number) => {
        return cfas.find((cfa) => cfa.id === id);
    };

    return (
        <>
            <Table
                columns={columns}
                dataSource={cfas.map((row) => ({ ...row, key: row.id, issuer: row.user.name }))}
                onRow={(row) => ({ onClick: () => showDrawer(row.id) })}
                loading={loading}
            />

            <Drawer
                title='Подробнее про ЦФА'
                placement='right'
                size={'large'}
                onClose={onClose}
                open={isDrawerOpen}
            >
                {getCfaImageById(selectedRowId) && (
                    <CfaDetails cfaImage={getCfaImageById(selectedRowId) as CfaImage} />
                )}
            </Drawer>
        </>
    );
};

export default CfaList;
