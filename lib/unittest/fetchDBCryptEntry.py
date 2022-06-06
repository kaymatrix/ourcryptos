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
each = crypts.CryptsEntry()

obj = support.CryptEntrySupport()
data = obj.dbEntryData

passcnt = 0
failcnt = 0
waitingcnt = 0
ttlcnt = 0
for each in data:
    tls.info(each.entrydate, each.symbol, each.status, each.exitdate)
    ttlcnt += 1
    if each.status == 'pass': passcnt += 1
    if each.status == 'fail': failcnt += 1
    if each.status == 'waiting': waitingcnt += 1


percent = passcnt/ttlcnt * 100
info = ''
info += '\n'
info += f'\n{tls.getDateTime()}'
info += f'\nPass: {passcnt}'    
info += f'\tFail: {failcnt}'
info += f'\tWaiting: {waitingcnt}'
info += f'\tTotal: {ttlcnt}'
info += f'\nPercentage: {percent}%'
info += '\n'
tls.info(info)

'''

2022-06-06 07:12:42
Pass: 69    Fail: 22    Waiting: 0    Total: 91
Percentage: 75.82417582417582%






'''