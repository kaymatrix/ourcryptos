'''
Created on 23-May-2022

@author: kayma

Run on specific time - morning 8.45 daily

get current bought list
get pass status,
get old fail status,
check status of the bought item

for eachboughtitem in boughtlist
    buyDate, buyTime, buySymbol, invested = perItemBuyAmnt, profitExpected, status=wait
    if status wait
        #{'symbol': 'ZRX', 'entrydate': '2022-04-22', 'entryprice': 0.9012, 'percentchange': -11.29626258, 'targetprice': 0.928236, 'status': 'fail', 'exitdate': '2022-04-28'}
        syminfo = get tracker info of symbol(buySymbol, entrydate == buydate, status = pass)
        if syminfo[pass] or exidate!='':
        (if pass or old fail.)
            currentBalance =     currentBalance + perItemBuyAmnt
            profitBalance = profitBalance + profitExpected
            eachboughtitem['status'] = pass
    
find 3 symbol
decide how much to invest and buy with balance

currentBalance >=  openBalance
    perSessionBuyAmnt = currentBalance / 2        (For morning/ For evening)
    itemFoundForSession
    
    perItemBuyAmnt = itemFoundForSession/perSessionBuyAmnt
    
    for eachItemFoundForSession
        'targetprice': 8.89302, 
        'entryprice': 8.634, 
        
        profitExpected = ((perItemBuyAmnt/entryprice)*targetprice)-perItemBuyAmnt
        
        boughtlist = buyDate, buyTime, buySymbol, invested = perItemBuyAmnt, profitExpected, status=wait - wait/passed
        
        currentBalance = currentBalance - perItemBuyAmnt
         
       


'''

from lib import tools
from decimal import Decimal
from lib.cryptlibs import trackers
from lib.cryptlibs import GCP_DATA_LIB as gdl
tls = tools.getGlobalTools()
#tls.setDebugging()

openBalance = 100          
minBuy = 15

cache1 = 'previewbuy'
currentBalance = openBalance
profitBalance = 0

offlineData = {}
offlineData['openBalance'] = openBalance
offlineData['currentBalance'] = currentBalance
offlineData['profitBalance'] = profitBalance
offlineData['buylist'] = []

offlineData = tls.readData(cache1, offlineData)

#Verify Old Status
updatedBoughtList = []
tls.info('Read old entry status...')
for eachBoughtItem in offlineData['buylist']:
    buyDate = eachBoughtItem['buyDate']
    buyTime = eachBoughtItem['buyTime'] #m/e
    buySymbol = eachBoughtItem['buySymbol']
    invested = eachBoughtItem['invested']
    profitExpected = eachBoughtItem['profitExpected']
    status = eachBoughtItem['status']
    
    if status == 'waiting':
        entryCurrentStatus = gdl.getSpecificSymbolInfo(buySymbol, buyDate, buyTime)
        #{'symbol': 'XMR', 'entryprice': 264.6, 'percentchange': -7.9891164, 'entrydate': '2022-04-23', 'targetprice': 272.538, 'exitdate': '2022-04-23', 'status': 'pass'}
        tls.info(f'Checking old entry {buySymbol} bought on {buyDate}')
        tls.info(entryCurrentStatus)
        if entryCurrentStatus and (entryCurrentStatus['status'] == 'pass' or entryCurrentStatus['exitdate'] != ''):
            #target hit

            updatedItem = {}
            updatedItem['buyDate'] = buyDate
            updatedItem['buyTime'] = buyTime
            updatedItem['buySymbol'] = buySymbol
            updatedItem['invested'] = invested
            updatedItem['profitExpected'] = profitExpected
            updatedItem['status'] = 'pass'
            updatedBoughtList.append(updatedItem)
            
            offlineData['currentBalance'] = offlineData['currentBalance'] + invested
            offlineData['profitBalance'] = offlineData['profitBalance'] + profitExpected            
          
        else:
            updatedBoughtList.append(eachBoughtItem)
    else:
        updatedBoughtList.append(eachBoughtItem)

offlineData['buylist'] = updatedBoughtList

#Find new Symbols
tls.info('New symbol addition')
if offlineData['currentBalance']>=minBuy:
    
    alreadyAdded = False
    for eachBoughtItem in offlineData['buylist']:
        if eachBoughtItem['buyDate'] == tls.getDateTime('%Y-%m-%d') and eachBoughtItem['buyTime'] == tls.getMorE():
            alreadyAdded = True
    
    if not alreadyAdded:
        newSymbolsFound = trackers.findSymbol()
        newSymbolsFound = newSymbolsFound['data']
        ttlSymbolsFound = len(newSymbolsFound)
        for eachSymbol in newSymbolsFound:
            if offlineData['currentBalance']>=minBuy:
                buyTime = tls.getMorE()
                symbol = eachSymbol[1]
                entryDate = eachSymbol[3]
                entryPrice = eachSymbol[4]
                exitPercent = eachSymbol[5]
                exitPrice = float(entryPrice + (Decimal((exitPercent/100)) * exitPercent))      
                profitExpected = ((minBuy/entryPrice)*Decimal(exitPrice))-minBuy
        
                buyItem = {}
                buyItem['buyDate'] = entryDate
                buyItem['buyTime'] = buyTime
                buyItem['buySymbol'] = symbol
                buyItem['invested'] = minBuy
                buyItem['profitExpected'] = profitExpected
                buyItem['status'] = 'waiting'
                
                offlineData['buylist'].append(buyItem)
                offlineData['currentBalance'] = offlineData['currentBalance'] - minBuy
                #buyDate, buyTime, buySymbol, invested = perItemBuyAmnt, profitExpected, status=waiting
                tls.info(f'Bought {symbol}') 
            else:
                tls.info(f'No balance to buy item {symbol}')
    else:
        tls.info(f'For today already added.')
else:
    tls.info(f'No balance to buy new item')

tls.info('Done!')

tls.storeData(cache1, offlineData)
tls.info()
tls.prittyPrint(offlineData)

        