'''
Created on 05-Jun-2022

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

obj = support.CryptEntrySupport()
obj.coinInfoAllDetail = True
obj.rule.entryPercent = 0

ces, cds = obj.getLiveEntries()
for each in ces:
    tls.info(each.entrydate, each.entrytime, each.symbol, each.entryprice, each.targetprice, each.status)