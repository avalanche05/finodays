import { ArrowUpOutlined } from '@ant-design/icons';
import { Card, Col, Row, Statistic, Table, Typography } from 'antd';
import { useEffect, useState } from 'react';
import { IStatisctics, IUserStatistics } from '../api/models';
import { useStores } from '../hooks/useStores';

const Statistics = () => {
    const { rootStore } = useStores();
    const [statistics, setStatistics] = useState<IStatisctics | null | void>(null);
    const [usersStatistics, setUsersStatistics] = useState<IUserStatistics[] | null | void>(null);

    useEffect(() => {
        async function fetchProfile() {
            const fetchedStatistics = await rootStore
                .getStatistics()
                .catch((error) => console.log(error));

            const fetchedUsersStatistics = await rootStore
                .getUsersStatistics()
                .catch((error) => console.log(error));

            setStatistics(fetchedStatistics);
            setUsersStatistics(fetchedUsersStatistics);
        }
        fetchProfile();
    }, [rootStore]);

    return (
        <>
            <Row>
                <Typography.Title level={2}>Статистика за время конференции</Typography.Title>
            </Row>

            <Row gutter={[16, 16]}>
                <Col md={{ span: 8 }} span={24}>
                    <Card bordered={false}>
                        <Statistic
                            title='ЦФА выпущено'
                            value={statistics?.created_cfa_count}
                            precision={0}
                        />
                    </Card>
                </Col>
                <Col md={{ span: 8 }} span={24}>
                    <Card bordered={false}>
                        <Statistic
                            title='Количество операций'
                            value={statistics?.transactions_count}
                            precision={0}
                        />
                    </Card>
                </Col>
                <Col md={{ span: 8 }} span={24}>
                    <Card bordered={false}>
                        <Statistic
                            title='Оборот'
                            value={statistics?.turn}
                            precision={0}
                            suffix='₽'
                        />
                    </Card>
                </Col>
            </Row>

            <Row>
                <Col md={{ span: 8 }} span={24}>
                    {statistics?.created_cfa_count_increment ? (
                        <Card bordered={false}>
                            <Statistic
                                title='ЦФА выпущено за последний час'
                                value={statistics?.created_cfa_count_increment}
                                precision={2}
                                valueStyle={{ color: '#cf1322' }}
                                prefix={<ArrowUpOutlined />}
                            />
                        </Card>
                    ) : null}
                </Col>
                <Col md={{ span: 8 }} span={24}>
                    {statistics?.transactions_count_increment ? (
                        <Card bordered={false}>
                            <Statistic
                                title='ЦФА выпущено за последний час'
                                value={statistics?.transactions_count_increment}
                                precision={2}
                                valueStyle={{ color: '#cf1322' }}
                                prefix={<ArrowUpOutlined />}
                            />
                        </Card>
                    ) : null}
                </Col>
                <Col md={{ span: 8 }} span={24}>
                    {statistics?.turn_increment ? (
                        <Card bordered={false}>
                            <Statistic
                                title='ЦФА выпущено за последний час'
                                value={statistics?.turn_increment}
                                precision={2}
                                valueStyle={{ color: '#cf1322' }}
                                prefix={<ArrowUpOutlined />}
                            />
                        </Card>
                    ) : null}
                </Col>
            </Row>

            <Row>
                <Typography.Title style={{ marginTop: 40 }} level={2}>
                    Статистика пользователей
                </Typography.Title>
            </Row>

            <Row>
                <Typography.Title level={4} style={{ marginTop: 20 }}>
                    Топ 10 пользователей по обороту
                </Typography.Title>
            </Row>

            <Row gutter={[16, 16]}>
                <Table
                    style={{ width: '100%' }}
                    dataSource={usersStatistics
                        ?.sort((a, b) => a.buy_value - b.buy_value)
                        .slice(0, 10)
                        .map(({ name, buy_value, id }) => ({
                            name,
                            buy_value,
                            key: id,
                        }))}
                    columns={[
                        { title: 'Пользователь', dataIndex: 'name', key: 'name' },
                        { title: 'Оборот в ₽', dataIndex: 'buy_value', key: 'buy_value' },
                    ]}
                    pagination={false}
                />
            </Row>

            <Row>
                <Typography.Title level={4} style={{ marginTop: 20 }}>
                    Топ 10 пользователей по количеству операций
                </Typography.Title>
            </Row>

            <Row gutter={[16, 16]}>
                <Table
                    style={{ width: '100%' }}
                    dataSource={usersStatistics
                        ?.sort((a, b) => a.buy_count - b.buy_count)
                        .slice(0, 10)
                        .map(({ name, buy_count, id }) => ({
                            name,
                            buy_count,
                            key: id,
                        }))}
                    columns={[
                        { title: 'Пользователь', dataIndex: 'name', key: 'name' },
                        { title: 'Количество операций', dataIndex: 'buy_count', key: 'buy_count' },
                    ]}
                    pagination={false}
                />
            </Row>
        </>
    );
};

export default Statistics;
