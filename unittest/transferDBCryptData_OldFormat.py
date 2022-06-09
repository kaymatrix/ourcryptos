'''
Created on 03-Jun-2022

@author: kayma
'''
import os,sys
from lib import xtools
tls = xtools.getGlobalTools()
from lib.cryptlibs import crypts
from lib.cryptlibs import datastores
from lib.cryptlibs import exchanges
from lib.cryptlibs import support
from lib.cryptlibs import actions
from lib.cryptlibs import rules
from lib import gcp 
import pickle

forceGCP = 0

tls.setDebugging()
tls.setGlobalSwitch('forceGCP', forceGCP)


#---------------------------------

pickFrom = 'G:/pythonworkspace/ourcryptos/data/cache/20220609'
d = open(pickFrom,'rb')
data = pickle.load(d)
d.close()

inputlist = []
for each in data:
    dt = each.split('_')[0]
    tim = each.split('_')[1]
    info = data[each]
    
    symbol = info['symbol']
    percentchange = info['perchg']
    
    #tls.info((dt, tim, symbol, percentchange))
    inputlist.append((dt, tim, symbol, percentchange))


def _getItem(symbol,date,tim):
    for each in inputlist:
        if symbol == each[2] and date == each[0] and tim == each[1]:
            return each
    return None
        
#---------------------------------    


each = crypts.CryptsData()
obj = support.CryptDataSupport()

for each in obj.dbData:
    if each.percent_change == None:
        info = _getItem(each.symbol, each.entrydate, each.entrytime)
        if info:
            dt, tim, symbol, percentchange = info
            if symbol == each.symbol and dt == each.entrydate and tim == each.entrytime:
                id_ = obj.dbData.index(each)
                obj.dbData[id_].percent_change = percentchange
                #tls.info(f'Updated {each.symbol}!')
            else:
                info = _getItem(each.symbol, each.entrydate, each.entrytime)
                tls.info(f'Unable to find for {each.symbol} {each.entrydate} {each.entrytime} - {symbol} ' )
        else:
            tls.info(f'Unable to find for {each.symbol} {each.entrydate} {each.entrytime}' )

            
#obj.des.datas = obj.dbEntryData                
#obj.des.storeData()                
            
    
    