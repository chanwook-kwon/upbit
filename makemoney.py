import pyupbit
from pyupbit.quotation_api import get_tickers
import requests
import jwt
import time
import pandas as pd
import numpy as np

access = "8BVxcVc5ahBZv6bnT4vGS5cfoaY7bDoxso8CFcD8"          # 본인 값으로 변경
secret = "XS3k2r64b5LxxoNN4dsAxxGxEtWPgLJVKy0CyI05"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)

#매수목표금액 = 현재가격의 -0.4%
#매수목표금액 = 매수금액의 +0.5%

Coin_ADA = 'KRW-ADA'
ADA_Current_Price = pyupbit.get_current_price(Coin_ADA) #현재 코인 가격.
ADA_OneStep_Price = 1
ADA_OneStep_Percent = 0.16
ADA_Buy_Step = 3 #3*0.16% = 0.48% 현재 가격의 0.48%에 매수함.
ADA_Sell_Step = 4 #4*0.16 = 0.54% - 현재 가격의 0.54%에 매도함.
ADA_Buy_Money = 5500 # 1회 매수금액
ADA_Buy_Price = ADA_Current_Price-(ADA_Buy_Step*ADA_OneStep_Price)
ADA_Buy_Quantity = ADA_Buy_Money / ADA_Buy_Price
ADA_Try_Count = 0
ADA_Buy_Count = 0
ADA_Sell_Count = 0

print("current price=",ADA_Current_Price)

#무한루프
# if 보유한 코인이 있는가?(매수했냐?)
#    true : 보유한 코인이 있으면 매도하자. MA30 < MA60 으면 시장가 매도.(만약 매수가 >= 시장가라도 매도한다 )
#    false : 보유 코인이 없으면 매수해야하니 MA30 > MA60 인지 확인해서 true 일때 매수한다.(시장가)
while True:
    try:
        ADA_Balance = upbit.get_balance(ticker=Coin_ADA) #보유코인수량확인.
        ADA_Ma30 = pyupbit.get_ohlcv(Coin_ADA, interval = 'minute5', count=30)
        ADA_Ma60 = pyupbit.get_ohlcv(Coin_ADA, interval = 'minute5', count=60)
        ADA_Average_Ma30 = np.mean(ADA_Ma30['close'])
        ADA_Average_Ma60 = np.mean(ADA_Ma60['close'])
        if (ADA_Balance > 0) and (abs(ADA_Average_Ma60 - ADA_Average_Ma30) >= 0.5) : #보유코인이 있으면 매도한다.(이익일수도 있고, 손절일수도 있고)
            ADA_ret_Sell = upbit.sell_market_order(Coin_ADA,ADA_Balance)
            print("매도성공",ADA_ret_Sell)
            ADA_Sell_Count = ADA_Sell_Count + 1
        if (ADA_Balance == 0) and (abs(ADA_Average_Ma30 - ADA_Average_Ma60) >= 0.5) : #보유코인이 없으면 -> 매수 진행.
            ADA_ret_buy = upbit.buy_market_order(Coin_ADA,ADA_Buy_Money)
            print("매수성공",ADA_ret_buy)
            ADA_Buy_Count = ADA_Buy_Count + 1
        else :
            print("ADA_현재가=",ADA_Current_Price)
            print("ADA_Balance=",ADA_Balance)
            print("ADA_Average_Ma30=",ADA_Average_Ma30)
            print("ADA_Average_Ma60=",ADA_Average_Ma60)
            print("매수조건 Ma30-Ma60=",abs(ADA_Average_Ma30-ADA_Average_Ma60))
            print("매도조건 Ma30-Ma60=",abs(ADA_Average_Ma60-ADA_Average_Ma30))
            ADA_Try_Count = ADA_Try_Count + 1
            print("ADA_Try_Count=",ADA_Try_Count)
            print("ADA_Buy_Count=",ADA_Buy_Count)
            print("ADA_Sell_Count=",ADA_Sell_Count)
            print("----------------------------")
            time.sleep(10)
    except Exception as e:
            print(e)
            time.sleep(1)