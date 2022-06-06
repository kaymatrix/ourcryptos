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

each = crypts.CryptsData()

#ds = datastores.CryptDataStore()
#ds.gcPickleName = ds.gcPickleName
#ds.loadData()
#data = ds.datas

obj = support.CryptDataSupport()
data = obj.dbData
data = obj.filterByDateTime('20220603', inputList = data)
#data = obj.filterByPlusPercentage(inputList = data)
# chkForDate = tls.getDateCalc(3 * -1,'%Y%m%d')
#data = obj.filterByDateTime(chkForDate, inputList = data)

for each in data:
    tls.info(each.entrydate, each.entrytime, each.symbol, each.percentage_change)
tls.info(f'Count: {len(data)}')