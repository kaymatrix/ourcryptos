'''
Created on 26-Apr-2022

@author: kayma
'''
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from lib.cryptolibs import exchanges
from lib import tools

from binance import enums as en

en.ORDER_TYPE_LIMIT


tls = tools.Tools()
bn = exchanges.Binance()
gn = exchanges.General()

#tst = bn.bclient.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_5MINUTE, "1 day ago UTC")
#for each in tst:
#    print(each)

client = bn.bclient


def getBalance(coin):
    '''
    {'asset': 'USDT', 'free': '6.24220816', 'locked': '0.00000000'}
    input #6.24220816
    BNB: 0.00940287
    '''
    info = client.get_asset_balance(asset=coin)
    #tls.prittyPrint(info['balances'])
    if 'asset' in info and 'free' in info:
        bal = float(info['free'])
        return bal
    return 0.0

def accountActive():
    '''
    {'data': 'Normal'}

    '''
    info = client.get_account_status()
    info2 = client.get_account_api_trading_status()
    return 'data' in info and info['data'] == 'Normal' and 'data' in info2 and 'isLocked' in info2['data'] and info2['data']['isLocked'] == False


def placeBuyOrder(coin, buyPrice=0.0, sellPrice=0.0, forUSDT=0.0):
    '''
    While buying mention the take profit
    
    '''
    
    return client.create_test_order()

def placeStopLoss():
    pass


coin = 'SCRT'
buyPrice = 4.450
sellPrice = tls.getPercentIncrease(buyPrice, 3)
forUSDT = 3

r = placeBuyOrder(coin,buyPrice,sellPrice,forUSDT)
tls.prittyPrint(r)

#r = client.get_asset_details()
#client.create_order()()
#r = accountActive()
#tls.prittyPrint(r)

#bal = getBalance('BNB')
#tls.info(bal)
