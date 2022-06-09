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

forceGCP = 0

tls.setDebugging()
tls.setGlobalSwitch('forceGCP', forceGCP)

each = crypts.CryptsEntry()
obj = support.CryptEntrySupport()
data = obj.dbEntryData

passcnt = 0
failcnt = 0
waitingcnt = 0
ttlcnt = 0
for each in data:
    tls.info(each.entrydate, each.entrytime, each.percent_change, each.symbol, each.status, each.exitdate)
    ttlcnt += 1
    if each.status == 'pass': passcnt += 1
    if each.status == 'fail': failcnt += 1
    if each.status == 'waiting': waitingcnt += 1

tls.info('\n\nFail\n')
for each in data:
    if each.status == 'fail':
        tls.info(each.entrydate, each.symbol, each.status, each.exitdate)    

tls.info('\n\nWaiting\n')
for each in data:
    if each.status == 'waiting':
        tls.info(each.entrydate, each.symbol, each.status, each.exitdate)    

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

2022-06-06 09:39:05
Pass: 69    Fail: 22    Waiting: 1    Total: 92
Percentage: 75.0%

2022-06-07 05:21:38
Pass: 70    Fail: 21    Waiting: 1    Total: 93
Percentage: 75.26881720430107%

2022-06-07 18:17:34
Pass: 70    Fail: 21    Waiting: 4    Total: 96
Percentage: 72.91666666666666%

'''