'''
Created on 17-Mar-2022

@author: kayma
'''
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from lib import tools
from lib.cryptlibs import exchanges
tls = tools.getGlobalTools()
bn = exchanges.Binance()

coin = 'aave'
pair = 'USDT'
symbol = coin.upper().strip()+pair.upper().strip()

tst = bn.bclient.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE, "1 day ago UTC")
print(tst)

print('dones')

