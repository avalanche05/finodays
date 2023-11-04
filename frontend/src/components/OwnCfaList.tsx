import { useState } from 'react';
import { Button, Drawer, Space, Table } from 'antd';
import type { ColumnsType } from 'antd/es/table';
import { CfaImage, OwnCfaImage } from '../api/models';
import OwnCfaDetails from './OwnCfaDetails';

type Props = {
    cfas: OwnCfaImage[];
};

const OwnCfaList = ({ cfas }: Props) => {
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
                            Создать оффер
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
        return cfas.find((cfa) => cfa.cfa_image.id === id);
    };

    return (
        <>
            <Table
                columns={columns}
                dataSource={cfas.map((row) => ({
                    ...row.cfa_image,
                    key: row.cfa_image.id,
                    issuer: row.cfa_image.user.name,
                    count: row.tokens.length,
                }))}
                onRow={(row) => ({ onClick: () => showDrawer(row.id) })}
            />

            <Drawer
                title='Подробнее про ЦФА'
                placement='right'
                size={'large'}
                onClose={onClose}
                open={isDrawerOpen}
            >
                {getCfaImageById(selectedRowId) && (
                    <OwnCfaDetails ownCfaImage={getCfaImageById(selectedRowId) as OwnCfaImage} />
                )}
            </Drawer>
        </>
    );
};

export default OwnCfaList;
