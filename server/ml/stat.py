from data import trade, db_session

import numpy as np
from sklearn import preprocessing
import pandas as pd


import logging
from catboost import CatBoostRegressor
from datetime import datetime


db_session.global_init("../db/db.db")
db_sess = db_session.create_session()
trades = db_sess.query(trade.Trade).all()


min_max_scaler = preprocessing.MinMaxScaler()
model = CatBoostRegressor().load_model("model_weights")


def get_list_of_prices(cfa_token: int)->list:
    '''
    It has to find prices in trades
    
    cfa_id: id of cfa
    return: past price
    '''
    
    req = f'''
    SELECT trade.price
    FROM trade
    WHERE trade.cfa_token = {cfa_token}
    '''
    
    
    x = [0.4, 0.5, 0.6]
   
    if not(any(x)): #if all zeros
        logging.warning(f"stat.py-> {cfa_token}: When loading prices all data zeros")

    return x   



def refit_model(list_of_prices, period: int=10):
    '''
    Retrain base model on data in list_of_prices. Returns nothing, just rewrite model weights
    
    Warninig! Model weights depend on period
    '''

    if len(list_of_prices) < period:
        logging.warning("Fail to train model, too small list_of_prices. Or you can make period less")
        return
    
    x = np.array(list_of_prices).reshape(-1,1)
    scaled = min_max_scaler.fit_transform(x)
    
    objs =[]

    for i in range(0, len(scaled)-period-1):
        obj = pd.Series(scaled[i:i+period+1])
        objs.append(obj)

    df = pd.concat(objs, axis=1)
    df = df.T

    if len(df.columns[:-1])!=period:
        logging.warning("Mismatching sizes of train set. Error handled by human")
    
    X = df.drop([df.columns[-1]], axis=1)
    y = df[df.columns[-1]]
    
    model.fit(X, y, verbose=1000)
    model.save_model(f"./ws/model_weights:{str(datetime.now())}")



def get_future_prices(cfa_token: int, is_refit: bool=False)->list:
    '''
    Return price(one element array) or prices depend on cfa_token
    
    cfa_id: id of cfa
    refit: whether to train the model to new data 
    
    return: future prices

    '''
    period = 10
    list_of_prices = get_list_of_prices(cfa_token=cfa_token)
    
    if is_refit:
        refit_model(list_of_prices=list_of_prices, period=period)
    
    prices = model.predict(list_of_prices[-period:])
    
    return list(prices)

