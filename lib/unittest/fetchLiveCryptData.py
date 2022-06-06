'''
Created on 03-Jun-2022

@author: kayma
'''
from lib.cryptlibs import crypts
from lib.cryptlibs import datastores
from lib.cryptlibs import exchanges
from lib.cryptlibs import support
from lib.cryptlibs import rules
from lib import gcp 
from lib import xtools
tls = xtools.getGlobalTools()
tls.setDebugging()

obj = support.CryptDataSupport()
obj.coinInfoAllDetail = True


data = obj.getLiveToppers() 
#data = obj.filterByDateTime('20220531', 'e', inputList = data)
#data = obj.filterByPlusPercentage(inputList = data)
# chkForDate = tls.getDateCalc(3 * -1,'%Y%m%d')
#data = obj.filterByDateTime(chkForDate, inputList = data)
for each in data:
    tls.info(each.entrydate, each.entrytime, each.symbol, each.percentage_change)