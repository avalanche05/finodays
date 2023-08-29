import logging

import numpy as np
import pandas as pd
from catboost import CatBoostRegressor

from data.cfa import Cfa
from data.trade import Trade


model = CatBoostRegressor().load_model("ml/ws/model_weights")



def predict_price(cfa_image_id, db_sess, is_refit=True, n_days=1):
    l = get_future_prices(cfa_image_id=cfa_image_id, db_sess=db_sess, is_refit=is_refit, n_days=n_days)
    return l


def get_future_prices(cfa_image_id, db_sess, is_refit: bool=True, n_days: int=1)->list:
    '''
    Return price(one element array) or prices depend on cfa_image_id
    
    cfa_id: id of cfa
    refit: whether to train the model to new data (default=True)
    n_days: predict prices for a few days (default=1)
    
    return: list of prices
    '''
    global model
    period = 10
    list_of_prices = get_list_of_prices(cfa_image_id=cfa_image_id, db_sess=db_sess)

    if list_of_prices == []:
        logging.warning("Data is null")
        return np.zeros(n_days).astype(list)
    
    if is_refit:
        refit_model(list_of_prices=list_of_prices, period=period)
        
    list_of_prices = preprocess_list(list_of_prices)
    
    n_predicted_prices = []
    
    for i in range(n_days):
    
        predicted_price = model.predict(list_of_prices[-period:])
        list_of_prices.append(predicted_price)
        n_predicted_prices.append(predicted_price)
        
    return n_predicted_prices


def get_list_of_prices(cfa_image_id, db_sess)->list:
    '''
    It has to find prices in trades
    
    cfa_id: id of cfa
    return: past price
    '''
    
    x = []
    
    trades = db_sess.query(Trade).all()
    cfas = db_sess.query(Cfa).filter(Cfa.cfa_image_id == cfa_image_id)

    cfas_tokens = set()
    
    for _cfa in cfas:
        cfas_tokens.add(_cfa.token)

    for _trade in trades:
        if _trade.cfa_token in cfas_tokens:
            x.append(_trade.price)

    if not(any(x)) or x is None: 
        logging.warning(f"stat.py-> {cfa_image_id}: When loading prices error occurred")

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
    
    

if __name__ == '__main__':
    n_days = 2
    
    l = get_future_prices(cfa_image_id=3, is_refit=True, n_days=n_days)
    print(l)

