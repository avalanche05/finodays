import smtplib, ssl

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "cfamarket.notifications@gmail.com"
password = "tktcsiqnfcmbidvt"
message_for_seller = """Subject: Уведомление о продаже ЦФА через наше приложение

Уважаемый {seller_name},

Мы надеемся, что вы в порядке. Мы хотели бы поделиться важной информацией относительно вашего ЦФА (Ценной Финансовой Активности), размещенного на нашей платформе.

С радостью хотим сообщить, что ваш ЦФА был успешно приобретен другим пользователем через наше приложение. Сделка завершена, и все необходимые транзакции и документы были обработаны.

Важно отметить следующие детали сделки:

Имя продавца: {seller_name} {seller_username}
Имя покупателя: {buyer_name} {buyer_username}
Дата сделки: {date}
Сумма сделки: {amount}

Эта успешная сделка является отличным примером эффективной работы нашей платформы, и мы надеемся, что она оказалась взаимовыгодной для всех сторон.

Если у вас возникнут вопросы или потребуется дополнительная информация, не стесняйтесь связаться с нами. Мы всегда готовы помочь вам в любых вопросах, связанных с использованием нашего приложения.

Мы благодарим вас за то, что выбрали нашу платформу для проведения этой сделки, и надеемся на долгосрочное сотрудничество. Если у вас есть еще активы, которые вы хотели бы предложить на продажу, не стесняйтесь добавить их на нашу платформу.

С уважением,

CFA Market"""
message_for_buyer = """Subject: Уведомление о покупке ЦФА через наше приложение

Уважаемый {buyer_name},

Надеемся, что у вас все хорошо. Мы хотим вам сообщить об успешной покупке ЦФА (Ценной Финансовой Активности) через наше приложение.

Мы рады подтвердить, что другой пользователь нашей платформы успешно продал вам необходимые ЦФА. Сделка была завершена, и все соответствующие транзакции и документы были обработаны в соответствии с нашими стандартами.

Пожалуйста, обратите внимание на следующие детали сделки:

Имя продавца: {seller_name} {seller_username}
Имя покупателя: {buyer_name} {buyer_username}
Дата сделки: {date}
Сумма сделки: {amount}

Это отличный пример успешной сделки на нашей платформе, и мы надеемся, что она полностью соответствует вашим ожиданиям.

Если у вас возникнут какие-либо вопросы или вам потребуется дополнительная информация, пожалуйста, не стесняйтесь связаться с нашей службой поддержки. Мы готовы помочь вам в любом вопросе, связанном с использованием нашего приложения.

Спасибо за использование нашей платформы для вашей финансовой активности. Мы надеемся, что вы останетесь довольны нашими услугами и рассмотрите возможность совершения дополнительных сделок в будущем.

С наилучшими пожеланиями,

CFA Market"""
message_for_initiator = """Subject: Уведомление о принятии вашего предложения через наше приложение

Уважаемый {initiator_name},

Мы надеемся, что у вас всё хорошо. Мы рады вам сообщить, что ваше предложение было успешно принято другим пользователем нашего приложения.

Пожалуйста, обратите внимание на следующие детали сделки:

Имя инициатора: {initiator_name} {initiator_username}
Имя принимающего: {host_name} {host_username}
Дата принятия предложения: {date}

Эта успешная сделка подтверждает эффективность нашей платформы и способность пользователям находить в ней взаимовыгодные возможности.

Если у вас возникнут какие-либо вопросы или вам потребуется дополнительная информация по данной сделке или использованию нашего приложения, не стесняйтесь обращаться к нашей службе поддержки. Мы всегда готовы помочь вам.

Мы благодарим вас за использование нашей платформы и надеемся, что эта сделка принесет вам взаимную пользу. Если у вас есть еще предложения или возможности, которые вы хотели бы разместить на нашей платформе, не стесняйтесь делать это в будущем.

С наилучшими пожеланиями,

CFA Market"""


def send_email(receiver_email: str, message: str):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.encode('utf-8'))


def generate_message_for_seller(seller_name, seller_username, buyer_name, buyer_username, date, amount):
    return message_for_seller.format(seller_name=seller_name,
                                     seller_username=seller_username,
                                     buyer_name=buyer_name,
                                     buyer_username=buyer_username,
                                     date=date,
                                     amount=amount)


def generate_message_for_buyer(seller_name, seller_username, buyer_name, buyer_username, date, amount):
    return message_for_buyer.format(seller_name=seller_name,
                                    seller_username=seller_username,
                                    buyer_name=buyer_name,
                                    buyer_username=buyer_username,
                                    date=date,
                                    amount=amount)


def generate_message_for_initiator(initiator_name, initiator_username, host_name, host_username, date):
    return message_for_initiator.format(initiator_name=initiator_name,
                                        initiator_username=initiator_username,
                                        host_name=host_name,
                                        host_username=host_username,
                                        date=date)


if __name__ == '__main__':
    send_email('mihail.glazov2015@yandex.ru', generate_message_for_seller('1', '1', '1', '1', '1', 1))