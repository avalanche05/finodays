import pandas as pd
import json


def get_ishimoku_info(high_data: list, low_data: list, close_data: list, check_last: int = 96) -> dict:
    '''
    high_data or low_data : list of the highest or lowest prices in period(usualy 1 hour). It need to be more than 52 periods(lists lenght more than 52)
    close_data: list of close prices. If doesnt exist compute as avarage btw low and high - hardcode
    check_last : analyze check_last periods(default = 52)

    return: dict with info
    '''
    last_marker = 0

    info = {
        'is_buy': 0,
        'why':
        {
            'en': 'Keep',
            'ru': 'Держать'
        }
    }

    high_data = pd.Series(high_data, dtype=int)
    low_data = pd.Series(low_data, dtype=int)
    close_data = pd.Series(close_data, dtype=int)

    period9_high = high_data.rolling(window=9).max()
    period9_low = low_data.rolling(window=9).min()

    tenkan_sen = (period9_high + period9_low) / 2

    period26_high = high_data.rolling(window=26).max()
    period26_low = low_data.rolling(window=26).min()

    kijun_sen = (period26_high + period26_low) / 2

    senkou_span_a = ((tenkan_sen + kijun_sen) / 2).shift(26)

    period52_high = high_data.rolling(window=52).max()
    period52_low = low_data.rolling(window=52).min()

    senkou_span_b = ((period52_high + period52_low) / 2).shift(26)

    chikou_span = list(close_data.shift(-22))

    senkou_span_a = list(senkou_span_a)
    senkou_span_b = list(senkou_span_b)
    kijun_sen = list(kijun_sen)
    tenkan_sen = list(tenkan_sen)

    tenkan_more_kuijun = True

    for i in range(len(close_data) - check_last, len(close_data)):

        if tenkan_sen[i] is None or kijun_sen[i] is None:
            continue

        if tenkan_more_kuijun:

            if kijun_sen[i] > tenkan_sen[i]:  # crossing
                tenkan_more_kuijun = False

                if i > last_marker:
                    info['is_buy'] = 0
                    info['why']['en'] = 'Sell. Dead cross - depend on short distance'
                    info['why']['ru'] = 'Продавайте. Исходя из коротких дистанций'
                    last_marker = i


        elif not (tenkan_more_kuijun):

            if tenkan_sen[i] > kijun_sen[i]:  # crossing
                tenkan_more_kuijun = True

                if i > last_marker:
                    info['is_buy'] = 1
                    info['why']['en'] = 'Buy. Gold cross - depend on short distance'
                    info['why']['ru'] = 'Покупайте. Исходя из коротких дистанций'
                    last_marker = i

    A_more_B = True  # senkou

    for i in range(len(close_data) - check_last, len(close_data)):

        if senkou_span_a[i] is None or senkou_span_b[i] is None:
            continue

        if A_more_B:

            if senkou_span_b[i] > senkou_span_a[i]:  # crossing
                A_more_B = False

                if i > last_marker:
                    info['is_buy'] = 0
                    info['why']['en'] = 'Sell. Depend on medium distance'
                    info['why']['ru'] = 'Продавайте. Исходя из средних дистанций'
                    last_marker = i
                    print(i)


        elif not (A_more_B):

            if senkou_span_a[i] > senkou_span_b[i]:  # crossing
                A_more_B = True

                if i > last_marker:
                    info['is_buy'] = 1
                    info['why']['en'] = 'Buy. Depend on medium distance'
                    info['why']['ru'] = 'Покупайте. Исходя из средних дистанций'
                    last_marker = i
                    print(i)

    chikou_more_price = True  # chikou

    for i in range(len(close_data) - check_last, len(close_data)):

        if chikou_span[i] is None or close_data[i] is None:
            continue

        if chikou_more_price:

            if chikou_span[i] < close_data[i]:  # crossing
                chikou_more_price = False

                if i > last_marker:
                    info['is_buy'] = 0
                    info['why']['en'] = 'Sell. Depend on long distance'
                    info['why']['ru'] = 'Продавайте. Исходя из длинных дистанций'
                    last_marker = i

        elif not (chikou_more_price):

            if chikou_span[i] > close_data[i]:  # crossing
                chikou_more_price = True
                if i > last_marker:
                    info['is_buy'] = 1
                    info['why']['en'] = 'Buy. Depend on long distance'
                    info['why']['ru'] = 'Покупайте. Исходя из длинных дистанций'
                    last_marker = i

    info['why']['en'] += f'. {check_last - last_marker} periods ago was a marker'
    info['why']['ru'] += f'. {check_last - last_marker} периодов назад был маркер'

    return info
