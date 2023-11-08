import { ArrowUpOutlined } from '@ant-design/icons';
import { Card, Col, Row, Skeleton, Statistic, Table, Typography } from 'antd';
import { useEffect, useState } from 'react';
import { IStatisctics, IUserStatistics } from '../api/models';
import { useStores } from '../hooks/useStores';

const Statistics = () => {
    const { rootStore } = useStores();
    const [statistics, setStatistics] = useState<IStatisctics | null | void>(null);
    const [usersStatisticsCount, setUsersStatisticsCount] = useState<
        IUserStatistics[] | null | void
    >(null);
    const [usersStatisticsValue, setUsersStatisticsValue] = useState<
        IUserStatistics[] | null | void
    >(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    useEffect(() => {
        async function fetchProfile() {
            setIsLoading(true);

            const fetchedStatistics = await rootStore
                .getStatistics()
                .catch((error) => console.log(error));

            const fetchedUsersStatisticsCount = await rootStore
                .getUsersStatistics('count')
                .catch((error) => console.log(error));
            const fetchedUsersStatisticsValue = await rootStore
                .getUsersStatistics('value')
                .catch((error) => console.log(error));

            setStatistics(fetchedStatistics);
            setUsersStatisticsCount(fetchedUsersStatisticsCount);
            setUsersStatisticsValue(fetchedUsersStatisticsValue);
            setIsLoading(false);
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
                        {isLoading ? (
                            <Skeleton active paragraph={{ rows: 2 }} />
                        ) : (
                            <Statistic
                                title='ЦФА выпущено'
                                value={statistics?.created_cfa_count}
                                precision={0}
                            />
                        )}
                    </Card>
                </Col>
                <Col md={{ span: 8 }} span={24}>
                    <Card bordered={false}>
                        {isLoading ? (
                            <Skeleton active paragraph={{ rows: 2 }} />
                        ) : (
                            <Statistic
                                title='Количество операций'
                                value={statistics?.transactions_count}
                                precision={0}
                            />
                        )}
                    </Card>
                </Col>
                <Col md={{ span: 8 }} span={24}>
                    <Card bordered={false}>
                        {isLoading ? (
                            <Skeleton active paragraph={{ rows: 2 }} />
                        ) : (
                            <Statistic
                                title='Оборот'
                                value={statistics?.turn}
                                precision={0}
                                suffix='₽'
                            />
                        )}
                    </Card>
                </Col>

                <Col md={{ span: 8 }} span={24}>
                    {statistics?.created_cfa_count_increment ? (
                        <Card bordered={false}>
                            {isLoading ? (
                                <Skeleton active paragraph={{ rows: 2 }} />
                            ) : (
                                <Statistic
                                    title='ЦФА выпущено за последний час'
                                    value={statistics?.created_cfa_count_increment}
                                    precision={2}
                                    valueStyle={{ color: '#3f8600' }}
                                    prefix={<ArrowUpOutlined />}
                                />
                            )}
                        </Card>
                    ) : null}
                </Col>
                <Col md={{ span: 8 }} span={24}>
                    {statistics?.transactions_count_increment ? (
                        <Card bordered={false}>
                            {isLoading ? (
                                <Skeleton active paragraph={{ rows: 2 }} />
                            ) : (
                                <Statistic
                                    title='ЦФА выпущено за последний час'
                                    value={statistics?.transactions_count_increment}
                                    precision={2}
                                    valueStyle={{ color: '#3f8600' }}
                                    prefix={<ArrowUpOutlined />}
                                />
                            )}
                        </Card>
                    ) : null}
                </Col>
                <Col md={{ span: 8 }} span={24}>
                    {statistics?.turn_increment ? (
                        <Card bordered={false}>
                            {isLoading ? (
                                <Skeleton active paragraph={{ rows: 2 }} />
                            ) : (
                                <Statistic
                                    title='ЦФА выпущено за последний час'
                                    value={statistics?.turn_increment}
                                    precision={2}
                                    valueStyle={{ color: '#3f8600' }}
                                    prefix={<ArrowUpOutlined />}
                                />
                            )}
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
                    dataSource={usersStatisticsValue
                        ?.slice(0, 10)
                        .map(({ name, buy_value, sell_value, id }) => ({
                            name,
                            value: buy_value + sell_value,
                            key: id,
                        }))}
                    columns={[
                        { title: 'Пользователь', dataIndex: 'name', key: 'name' },
                        { title: 'Оборот в ₽', dataIndex: 'value', key: 'value' },
                    ]}
                    pagination={false}
                    loading={isLoading}
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
                    dataSource={usersStatisticsCount
                        ?.slice(0, 10)
                        .map(({ name, buy_count, sell_count, id }) => ({
                            name,
                            count: buy_count + sell_count,
                            key: id,
                        }))}
                    columns={[
                        { title: 'Пользователь', dataIndex: 'name', key: 'name' },
                        { title: 'Количество операций', dataIndex: 'count', key: 'count' },
                    ]}
                    pagination={false}
                    loading={isLoading}
                />
            </Row>
        </>
    );
};

export default Statistics;
