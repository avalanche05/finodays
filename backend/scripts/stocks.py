def client():
    from tinkoff.invest import Client, SecurityTradingStatus, CandleInterval
    from tinkoff.invest.services import InstrumentsService
    from tinkoff.invest.utils import quotation_to_decimal, now
    import pandas as pd
    from datetime import datetime

    from datetime import timedelta

    with Client('t.xSBxU2tajOvVGnB5Y_zA4CzZ91RfhABPZdBeET5RHoNma5uCqiJwUwxFBgT_0NESpl0Aw0_46Wb13wD0vEsbLw') as client:

        instruments: InstrumentsService = client.instruments
        tickers = []
        for method in ["shares", "bonds", "etfs", "currencies", "futures"]:
            for item in getattr(instruments, method)().instruments:
                tickers.append(
                    {
                        "name": item.name,
                        "ticker": item.ticker,
                        "class_code": item.class_code,
                        "figi": item.figi,
                        "uid": item.uid,
                        "type": method,
                        "min_price_increment": quotation_to_decimal(
                            item.min_price_increment
                        ),
                        "scale": 9 - len(str(item.min_price_increment.nano)) + 1,
                        "lot": item.lot,
                        "trading_status": str(
                            SecurityTradingStatus(item.trading_status).name
                        ),
                        "api_trade_available_flag": item.api_trade_available_flag,
                        "currency": item.currency,
                        "exchange": item.exchange,
                        "buy_available_flag": item.buy_available_flag,
                        "sell_available_flag": item.sell_available_flag,
                        "short_enabled_flag": item.short_enabled_flag,
                        "klong": quotation_to_decimal(item.klong),
                        "kshort": quotation_to_decimal(item.kshort),
                    }
                )

        tickers_df = pd.DataFrame(tickers)
        tickers_df.to_csv('tickers.csv')
        ticker = "LKOH"

        ticker_df = tickers_df[tickers_df["ticker"] == ticker]
        ticker_df.to_csv('our_ticker.csv')

        figis = list(ticker_df['figi'])
        print(figis)

        open_data = []
        high_data = []
        low_data = []
        close_data = []
        dates = []

        for candle in client.get_all_candles(
                figi=figis[0],
                from_=now() - timedelta(days=20),
                interval=CandleInterval.CANDLE_INTERVAL_HOUR, ):
            open_data.append(candle.open.units)
            high_data.append(candle.high.units)
            low_data.append(candle.low.units)
            close_data.append(candle.close.units)
            dates.append(candle.time)

        print(low_data)

client()