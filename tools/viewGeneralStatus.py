'''
Created on 17-Mar-2022


morning - 8.45 am
afternoon - 1.15 pm
evening - 5.30 pm


@author: kayma
'''
from lib import tools
from lib.cryptlibs import GCP_DATA_LIB as gdl
from lib.cryptlibs import exchanges
tls = tools.getGlobalTools()

cmc = exchanges.CoinMarketCap()
bn = exchanges.Binance()
gn = exchanges.General()

mode = tls.getArgValue('mode') #morning, afternoon, evening
isprod = tls.isArgPresent('prod')
isview = tls.isArgPresent('view')
isdebug  = tls.isArgPresent('debug')
today = tls.getDateTime('%Y-%m-%d')
nowtime = tls.getDateTime('%H:%M:%S %p')

#GoldRate
gld = gn.getGoldRate()

#USDRate
usdt = bn.getP2PRate()

#Dominance
dm = gn.getBTCDominance()

#Fear/Greed
dt, fg, fgtxt = gn.getFearGreedIndex()


#---------------------------------------------
tls.info('')
tls.info('-------------')
tls.info(f'Date: {today}{nowtime}')
tls.info(f'Gold: {gld} Rs')
tls.info(f'USDT: {usdt} Rs')
tls.info(f'BTC Dominance: {dm}%')
tls.info(f'Fear Greed Index: {fgtxt} - {fg}')
tls.info('-------------')    
tls.info('Done')
