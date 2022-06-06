'''
Created on 21-Mar-2022

@author: kayma

ApeCoin Price$8.00
Price Change24h$0.18372.35%
24h Low / 24h High$7.47 /$8.35
Trading Volume24h$662,045,836.471.75%
Volume / Market Cap0.2832
Market Dominance0.18%
Market Rank#32


'''


from lib import tools
from lib.cryptlibs import GCP_DATA_LIB as gdl
from lib.cryptlibs import exchanges
tls = tools.getGlobalTools()

coin = 'sand'
cmc = exchanges.CoinMarketCap()
info = cmc.getCoinInfo(coin)
tls.prittyPrint(info)
