import { Button, Card, Col, Row, Statistic, Typography } from 'antd';
import CfaList from '../components/CfaList';
import OffersList from '../components/OffersList';

const Profile = () => {
    return (
        <>
            <Typography.Title level={2}>Мой кабинет</Typography.Title>

            <Card>
                <Row gutter={16}>
                    <Col span={12}>
                        <Statistic title='Организация' value={'АО Ромашка'} />
                    </Col>
                    <Col span={12}>
                        <Statistic title='Баланс ₽' value={112893} precision={2} />

                        <Button style={{ marginTop: 16 }} type='primary'>
                            Пополнить
                        </Button>
                        <Button style={{ marginTop: 16, marginLeft: 16 }} type='default'>
                            Вывести
                        </Button>
                    </Col>
                </Row>
            </Card>

            <Typography.Title level={3} style={{ marginTop: 16 }}>
                Мои ЦФА
            </Typography.Title>

            <CfaList />

            <Typography.Title level={3} style={{ marginTop: 16 }}>
                Мои офферы
            </Typography.Title>

            <OffersList />
        </>
    );
};

export default Profile;
