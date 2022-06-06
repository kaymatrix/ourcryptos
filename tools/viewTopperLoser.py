'''
Created on 17-Mar-2022


morning - 8.45 am
afternoon - 1.15 pm
evening - 5.30 pm


@author: kayma
'''
from lib import tools
from lib.cryptlibs import exchanges
tls = tools.getGlobalTools()

cmc = exchanges.CoinMarketCap()
bn = exchanges.Binance()
gn = exchanges.General()
cp = exchanges.CryptoPanic()

today = tls.getDateTime('%Y-%m-%d')
nowtime = tls.getDateTime('%H:%M:%S %p')

def getMarketToppers():
        
    #Topgainer
    tg = cmc.getTopGainer()
    
    #Toploser
    tl = cmc.getTopLoser()
    
    toppers = tg + tl
    
    #Volumepercent
    vp = cmc.getMarketVolumeToper()
    
    def marketvoltopper(coin):
        for each in vp:
            if str(each[1]).upper() == str(coin).upper():
                return str(each[3])
        return 0       
    
    data = []
    for cnt,each in enumerate(toppers):
        symbol = each[2]
        perchg = each[3]                    #%%%
        ttlvols = each[5]
        binvol = marketvoltopper(symbol)    #%%%
        binvol = float(binvol)
        _pop = cp.getCoinInfo(symbol)
        usr_resp = _pop['ttlall']
        usr_weekcnt = _pop['weekcnt']
        usr_last2dayscnt = _pop['last2dayscnt']
        nw = (cnt, symbol, perchg, ttlvols, binvol, usr_resp, usr_weekcnt, usr_last2dayscnt)
        data.append(nw)
    
    return data
        

data = getMarketToppers()
for each in data:
    print(each)

print('done')



