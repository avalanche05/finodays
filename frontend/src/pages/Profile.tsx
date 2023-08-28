import { Button, Card, Col, InputNumber, Modal, Row, Statistic, Typography, message } from 'antd';
import { useEffect, useState } from 'react';
import { useStores } from '../hooks/useStores';
import { valueType } from 'antd/es/statistic/utils';
import { IProfile } from '../api/models/Profile';
import { Offer, OwnCfaImage } from '../api/models';
import OwnCfaList from '../components/OwnCfaList';
import OwnOffersList from '../components/OwnOffersList';

const Profile = () => {
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
    const [profileTrigger, setProfileTrigger] = useState<boolean>(false);
    const [cfas, setCfas] = useState<OwnCfaImage[]>([]);
    const [offers, setOffers] = useState<Offer[]>([]);

    useEffect(() => {
        async function fetchProfile() {
            const profile = await rootStore.getProfileInfo();
            const userCfas = await rootStore.getUserCfas(profile.id);
            const userOffers = await rootStore.getOffersByUser(profile.id);

            setProfile(profile);
            setCfas(userCfas);
            setOffers(userOffers);
        }
        fetchProfile();
    }, [rootStore, profileTrigger]);

    const deposit = () => {
        setConfirmLoading(true);

        rootStore
            .deposit(moneyAmount)
            .then(() => {
                messageApi.success('Баланс успешно пополнен');
                setProfileTrigger(!profileTrigger);
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
                messageApi.success('Баланс успешно пополнен');
                setProfileTrigger(!profileTrigger);
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
            <OwnCfaList cfas={cfas} trigger={setProfileTrigger} triggerValue={profileTrigger} />

            <Typography.Title level={3} style={{ marginTop: 16 }}>
                Мои офферы
            </Typography.Title>

            <OwnOffersList offers={offers} />

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
};

export default Profile;
