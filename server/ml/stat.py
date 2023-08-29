# from data import trade, db_session

import numpy as np
from sklearn import preprocessing
import pandas as pd
from sqlalchemy import select

import logging
from catboost import CatBoostRegressor
from datetime import datetime


# db_session.global_init("../db/db.db")
# db_sess = db_session.create_session()
# trades = db_sess.query(trade.Trade).all()


min_max_scaler = preprocessing.MinMaxScaler()
model = CatBoostRegressor().load_model("ml/ws/model_weights")


def get_list_of_prices(cfa_token: str)->list:
    '''
    It has to find prices in trades
    
    cfa_id: id of cfa
    return: past price
    '''
    
    sql_req = f'''
    SELECT trade.price
    FROM trade
    WHERE trade.cfa_token = {cfa_token}
    '''
    
    stmt = select(trade.c.price).where(trade.c.cfa_token == cfa_token)
    result = db_sess.execute(stmt)
    trade_prices = [row[0] for row in result]
    
    x = trade_prices
       
    if not(any(x)) or x is None: #
        logging.warning(f"stat.py-> {cfa_token}: When loading prices error occurred")

    return x   



def refit_model(list_of_prices, period: int=10):
    '''
    Retrain base model on data in list_of_prices. Returns nothing, just rewrite model weights
    
    Warninig! Model weights depend on period
    '''
    global model

    if len(list_of_prices) < period:
        logging.warning("Fail to train model, too small list_of_prices. Or you can make period less")
        return
    
    x = np.array(list_of_prices)
    
    objs =[]

    for i in range(0, len(x)-period-1):

        obj = pd.Series( x[i:i+period+1] )
        objs.append(obj)

    df = pd.concat(objs, axis=1)
    df = df.T

    if len(df.columns[:-1])!=period:
        logging.warning("Mismatching sizes of train set. Error handled by human")
    
    X = df.drop([df.columns[-1]], axis=1)
    y = df[df.columns[-1]]
    
    model.fit(X, y, verbose=1000)
    model.save_model(f"ml/ws/model_weights:refit")
    model = CatBoostRegressor().load_model("ml/ws/model_weights:refit")


def preprocess_list(list_of_prices, period: int=10)->list:
    
    x = list(list_of_prices[-period:])

    if len(x) != period:
        raise Exception("preprocess_list error with lenght")
    
    return x
    
    
def get_future_prices(cfa_token: str='', is_refit: bool=True, n_days: int=3)->list:
    '''
    Return price(one element array) or prices depend on cfa_token
    
    cfa_id: id of cfa
    refit: whether to train the model to new data (default=False)
    n_days: predict prices for a few days (default=1)
    
    return: list of prices
    '''
    global model
    
    period = 10
    
    # list_of_prices = get_list_of_prices(cfa_token=cfa_token)
    
    fake_data = [0.3, 0.4, 0.412, 0.44, 0.42, 0.39, 0.35, 0.32, 0.29, 0.38, 0.330, 0.28, 0.38, 0.44]
    
    if is_refit:
        refit_model(list_of_prices=fake_data, period=period)
        
    list_of_prices = preprocess_list(fake_data)
    
    n_predicted_prices = []
    
    for i in range(n_days):
    
        predicted_price = model.predict(list_of_prices[-period:])
        list_of_prices.append(predicted_price)
        
        n_predicted_prices.append(predicted_price)
        
    return n_predicted_prices

print(get_future_prices())
# db_sess.close()