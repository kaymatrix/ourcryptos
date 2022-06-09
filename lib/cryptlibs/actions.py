'''
Created on 02-Jun-2022

@author: kayma
'''
from lib.cryptlibs import crypts
from lib.cryptlibs import datastores
from lib.cryptlibs import exchanges
from lib.cryptlibs import support
from lib import gcp 
from lib import xtools
tls = xtools.getGlobalTools()

class CryptActions(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.tls = tls
        self.bn = exchanges.Binance()
        self.gio = exchanges.Giottus()
        self.wx = exchanges.Wazrix()
        self.gn= exchanges.General()
        self.cmc = exchanges.CoinMarketCap()
        self.crp = exchanges.CryptoPanic() 
        self.gcps = gcp.GCPSupport()
        self.ds = datastores.CryptDataStore()
        self.es = datastores.CryptEntryStore()
        self.cds = support.CryptDataSupport()        
        self.ces = support.CryptEntrySupport()
        
        self.today = tls.getDateTime('%Y%m%d')
        
        self.alertInfo = ''

    def helloWorld(self):
        self.tls.info('Thanks for calling hello world')
        return {"hi":"All good"}
    
    def _informAndReadyForAlert(self, info = ''):
        self.alertInfo +='\n' + info
        self.tls.info(info)
    
    def getLatestData(self, fetchGeneralData=1, fetchValidCoins=0, alert=1, storeToDB=0):
        resp = {}
        liveData = []
        liveEntry = []
        
        #General Data
        if fetchGeneralData:
            self.cds.filterPercentageChangeBelow = self.ces.rule.entryPercent
            liveData = self.cds.getLiveToppers()
            dbData = self.cds.dbData
            ttlData = liveData + dbData
        
            if storeToDB:
                self.ds.datas = ttlData
                self.ds.storeData()

            resp['CryptDataLive'] = len(liveData)
            resp['CryptDataDB'] = len(dbData)
            resp['CryptDataTotal'] = len(ttlData)                
    
            self._informAndReadyForAlert(f'No.of CryptDataLive: {len(liveData)}')
            self._informAndReadyForAlert(f'No.of CryptDataDB: {len(dbData)}')
            self._informAndReadyForAlert(f'No.of CryptDataTotal: {len(ttlData)}')
        
        #Valid Coin Data
        if fetchValidCoins:
            liveEntry, dbData = self.ces.getLiveEntries(3, liveData)
            dbEntries = self.es.datas
            ttlEntries = dbEntries + liveEntry

            if storeToDB:            
                self.es.datas = ttlEntries
                self.es.storeData() 

            resp['CryptEntryLive'] = len(liveEntry)
            resp['CryptEntryDB'] = len(dbEntries)
            resp['CryptEntryTotal'] = len(ttlEntries)
            resp['CryptEntryLiveData'] = []  
            for eachEntry in liveEntry:
                entry = [eachEntry.symbol,eachEntry.percent_change,eachEntry.entryprice]
                resp['CryptEntryLiveData'].append(entry)                     

            self._informAndReadyForAlert(f'No.of CryptEntryLive: {len(liveEntry)}')
            self._informAndReadyForAlert(f'No.of CryptEntryDB: {len(dbEntries)}')
            self._informAndReadyForAlert(f'No.of CryptEntryTotal: {len(ttlEntries)}')   
            
            self._informAndReadyForAlert(f'Current live entry:')
            for eachEntry in liveEntry:
                self._informAndReadyForAlert(f'\t{eachEntry.symbol},\n\tpercent: {eachEntry.percent_change}%,\n\trate: {eachEntry.entryprice} usdt')
            self._informAndReadyForAlert(f'-----------------')
                
        if alert:
            heading = 'TrackData Captured' if len(liveEntry)>0 else 'CryptData Captured'
            data = self.alertInfo 
            self.tls.info(data)
            self.tls.notify(heading, data, heading)
            
        return resp
    
    def checkEntries(self, alert=1, storeToDB=0):
        resp = {}
        hits = []
        fails = []
        waiting = []
        
        eachEntry = crypts.CryptsEntry()
        for inx, eachEntry in enumerate(self.ces.dbEntryData):
            symbol = eachEntry.symbol
            status = eachEntry.status
            entrydate = eachEntry.entrydate
            targetprice = eachEntry.targetprice
            waitDuration = self.ces.rule.waitDuration
            dateDiff = tls.getDateDiff(entrydate,self.today,'%Y%m%d')
            if status == 'waiting':
                info = f'Checking {symbol}, waiting for hit within {dateDiff} day(s)'
                self._informAndReadyForAlert(info)
                if dateDiff<waitDuration:
                    currentprice =  self.bn.getCoinPrice(symbol)
                    if currentprice>=targetprice:
                        self.ces.dbEntryData[inx].exitdate = self.today
                        self.ces.dbEntryData[inx].status = 'pass'
                        hits.append(self.ces.dbEntryData[inx])
                        info = f'{symbol} hit the target! in {dateDiff} day(s)'
                        self._informAndReadyForAlert(info)     
                    else:
                        waiting.append(self.ces.dbEntryData[inx])                                         
                else:
                    self.ces.dbEntryData[inx].status = 'fail'
                    fails.append(self.ces.dbEntryData[inx])
                    info = f'{symbol} failed as it was entered on {entrydate}'
                    self._informAndReadyForAlert(info)
                                       
            #Second attempt
            if status == 'fail':
                currentprice =  self.bn.getCoinPrice(symbol)
                if currentprice>=targetprice:
                    self.ces.dbEntryData[inx].exitdate = self.today
                    self.ces.dbEntryData[inx].status = 'delayed'
                    hits.append(self.ces.dbEntryData[inx])
                    info = f'{symbol} hit the target in delay of {dateDiff} day(s) after its fail!'                    
                    self._informAndReadyForAlert(info)

        hitCnt = len(hits)
        failCnt = len(fails)
        waitingCnt = len(waiting)
        resp['data'] = {}
        resp['data']['hit'] = hitCnt
        resp['data']['fail'] = failCnt
        resp['data']['waiting'] = waitingCnt
        
        if hitCnt > 0 or failCnt > 0:
            if alert:
                data = self.alertInfo                
                self.tls.info(data)
                header = f'{hitCnt} hit, {failCnt} fail, {waitingCnt} waiting' 
                self.tls.notify(header, data, header)
            
            if storeToDB:
                self.es.datas = self.ces.dbEntryData
                self.es.storeData()          
        
        return resp       

        