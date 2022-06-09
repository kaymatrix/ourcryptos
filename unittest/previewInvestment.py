'''
Created on 08-Jun-2022

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

each = crypts.CryptsData()

ces = support.CryptEntrySupport()
obj = support.CryptDataSupport()

alldates = []
for each in obj.dbData:
    tls.info(each.symbol, each.entrydate, each.entrytime, each.percent_change, each.
    if not each.entrydate in alldates: alldates.append(each.entrydate)

def _getInfoForDate(date, time):
    lst = []
    for each in obj.dbData:
        if each.entrydate == date and each.entrytime == time:
            lst.append(each)
    return lst  

alldates.sort()


for eachDate in alldates:
    
    #Morning    
    nowDate = eachDate
    nowTime = 'm'   
    nowDatas = _getInfoForDate(nowDate, nowTime)
    
    tls.info(f'Now: {nowDate} - {nowTime} - Entries: {len(nowDatas)}')
    
    if len(nowDatas):
        foundEntry = ces.getLiveEntries(3, nowDatas)
        print(foundEntry)    
    

'''
eachEntry = crypts.CryptsEntry()
obj = support.CryptEntrySupport()

entires = obj.dbEntryData
cdatas = obj.dbData

ttlInvest = 100
perSessionInvest = ttlInvest / 2
perSymbolInvest = perSessionInvest / 3

entriesDate = []
for each in entires:
    tls.info(each.symbol, each.entrydate, each.entrytime, each.percent_change)
    if not each.entrydate in entriesDate: entriesDate.append(each.entrydate)

def _getEntriesByDate(date, time):
    lst = []
    for each in entires:
        if each.entrydate == date and each.entrytime == time:
            lst.append(each)
    return lst     
    

for eachDate in entriesDate:
    
    #Morning    
    today = eachDate
    time = 'm'
    
    
    tls.info(f'Now: {today} _ {time}')
    todaysEntries = _getEntriesByDate(today,time)
    ttlEntries = len(todaysEntries)
    
    if ttlEntries == 2:
        nowPerSymbolInvest = (perSymbolInvest * 3) / 2
    elif ttlEntries == 1:
        nowPerSymbolInvest = perSymbolInvest * 3
    else:
        nowPerSymbolInvest = 0
    
    if nowPerSymbolInvest:
        for eachEntry in todaysEntries:
            buyqty = eachEntry.entryprice / perSymbolInvest
            tls.info(f'Buying: {buyqty} {eachEntry.symbol} for {perSymbolInvest} usdt')
            eachEntry.invested = 'waiting'
        
        
    
'''    
    


