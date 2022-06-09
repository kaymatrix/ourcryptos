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
symbol = 'EGLD'
entrydate = '20220606'

tls.setDebugging()
tls.setGlobalSwitch('forceGCP', forceGCP)

each = crypts.CryptsEntry()
obj = support.CryptEntrySupport()
data = obj.dbEntryData

for each in data:
    if symbol==each.symbol and entrydate == each.entrydate:
        tls.info(each)
