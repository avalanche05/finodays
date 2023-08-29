import {
    Alert,
    Button,
    Card,
    Col,
    InputNumber,
    Modal,
    Row,
    Statistic,
    Typography,
    message,
} from 'antd';
import { useEffect, useState } from 'react';
import { useStores } from '../hooks/useStores';
import { valueType } from 'antd/es/statistic/utils';
import { IProfile } from '../api/models/Profile';
import { Desire, Offer, OwnCfaImage } from '../api/models';
import OwnCfaList from '../components/OwnCfaList';
import OwnOffersList from '../components/OwnOffersList';
import OwnDesiresList from '../components/OwnDesiresList';
import { observer } from 'mobx-react-lite';
import OwnDealsTabs from '../components/OwnDeals';

const Profile = observer(() => {
    const [messageApi, contextHolder] = message.useMessage();
    const { rootStore } = useStores();
    const [openDepositModal, setOpenDepositModal] = useState(false);
    const [openWithdrawModal, setOpenWithdrawModal] = useState(false);
    const [confirmLoading, setConfirmLoading] = useState(false);
    const [moneyAmount, setMoneyAmount] = useState<number>(0);
    const [profile, setProfile] = useState<IProfile>({
        balance: 0,
        id: 0,
        login: '',
        name: '',
        username: '',
    });
    const [cfas, setCfas] = useState<OwnCfaImage[]>([]);
    const [offers, setOffers] = useState<Offer[]>([]);
    const [desires, setDesires] = useState<Desire[]>([]);

    useEffect(() => {
        async function fetchProfile() {
            const profile = await rootStore.getProfileInfo();
            const userCfas = await rootStore.getUserCfas(profile.id).catch(() => []);
            const userOffers = await rootStore.getOffersByUser(profile.id).catch(() => []);
            const userDesires = await rootStore.getDesiresByUser(profile.id).catch(() => []);

            setProfile(profile);
            setCfas(userCfas);
            setOffers(userOffers);
            setDesires(userDesires);
        }
        fetchProfile();
    }, [rootStore, rootStore.trigger]);

    const deposit = () => {
        setConfirmLoading(true);

        rootStore
            .deposit(moneyAmount)
            .then(() => {
                messageApi.success('Баланс успешно пополнен');
                rootStore.setTrigger();
            })
            .catch(() => {
                messageApi.error('Ошибка пополнения баланса');
            })
            .finally(() => {
                setOpenDepositModal(false);
                setConfirmLoading(false);
            });
    };

    const cancelDepositModal = () => {
        setOpenDepositModal(false);
    };

    const withdraw = () => {
        setConfirmLoading(true);
        rootStore
            .withdraw(moneyAmount)
            .then(() => {
                messageApi.success('Баланс успешно изменен');
                rootStore.setTrigger();
            })
            .catch(() => {
                messageApi.error('Ошибка изменения баланса');
            })
            .finally(() => {
                setOpenWithdrawModal(false);
                setConfirmLoading(false);
            });
    };

    const cancelWithdrawModal = () => {
        setOpenWithdrawModal(false);
    };

    const onMoneyAmountChange = (value: valueType | null) => {
        if (value) {
            setMoneyAmount(parseFloat(value.toString()));
        }
    };

    return (
        <>
            {contextHolder}
            <Typography.Title level={2}>Мой кабинет</Typography.Title>

            <Card>
                <Row gutter={16}>
                    <Col span={12}>
                        <Statistic title='Организация' value={profile.name} />
                    </Col>
                    <Col span={12}>
                        <Statistic title='Баланс ₽' value={profile.balance} precision={2} />

                        <Button
                            onClick={() => setOpenDepositModal(true)}
                            style={{ marginTop: 16 }}
                            type='primary'
                        >
                            Пополнить
                        </Button>
                        <Button
                            onClick={() => setOpenWithdrawModal(true)}
                            style={{ marginTop: 16, marginLeft: 16 }}
                            type='default'
                        >
                            Вывести
                        </Button>
                    </Col>
                </Row>
            </Card>

            <Typography.Title level={3} style={{ marginTop: 16 }}>
                Мои ЦФА
            </Typography.Title>
            <OwnCfaList cfas={cfas} />

            <Typography.Title level={3} style={{ marginTop: 16 }}>
                Мои офферы
            </Typography.Title>

            <Typography.Paragraph>
                В этой таблице представлены все ваши предложения на продажу ЦФА. Вы можете отменить
                любое из них.
            </Typography.Paragraph>

            <OwnOffersList offers={offers} />

            <Typography.Title level={3} style={{ marginTop: 16 }}>
                Мои заявки
            </Typography.Title>

            <Typography.Paragraph>
                В этой таблице представлены все ваши заявки на покупку ЦФА. Как только кто-то
                создаст оффер с ЦФА по вашей цене, они будут автоматически исполнены.
            </Typography.Paragraph>

            <OwnDesiresList desires={desires} />

            <Typography.Title level={3} style={{ marginTop: 16 }}>
                Мои сделки
            </Typography.Title>

            <Alert
                message='В данный момент в ui реализован только просмотр и отклонение сделок. Полный функционал для работы со сделками доступен в API'
                type='warning'
            />

            <Typography.Paragraph>
                В этой таблице представлены все ваши сделки - входящие и исходящие. Сделки - это
                предложения обмена между пользователями (обмен ЦФА на ЦФА). Вы можете отменить любую
                из них.
            </Typography.Paragraph>

            <OwnDealsTabs />

            <Modal
                title='Пополнить баланс'
                open={openDepositModal}
                onOk={deposit}
                confirmLoading={confirmLoading}
                onCancel={cancelDepositModal}
                okText='Пополнить'
                cancelText='Отмена'
            >
                <Typography.Paragraph>Тестовое пополнение баланса на сумму:</Typography.Paragraph>
                <InputNumber
                    onChange={onMoneyAmountChange}
                    style={{ width: '100%' }}
                    placeholder='Введите сумму'
                />
            </Modal>
            <Modal
                title='Вывести средства с баланса'
                open={openWithdrawModal}
                onOk={withdraw}
                confirmLoading={confirmLoading}
                onCancel={cancelWithdrawModal}
                okText='Вывысти'
                cancelText='Отмена'
            >
                <Typography.Paragraph>Тестовый вывод средств на сумму:</Typography.Paragraph>
                <InputNumber
                    onChange={onMoneyAmountChange}
                    style={{ width: '100%' }}
                    placeholder='Введите сумму'
                />
            </Modal>
        </>
    );
});

export default Profile;
