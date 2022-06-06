'''
Created on 31-May-2022

Crypto Data Store
for adding , loading, reading data
read,write

@author: kayma
'''
from lib.cryptlibs import crypts
from lib import gcp
from lib import xtools
tls = xtools.getGlobalTools()

class CryptDataStore():
    
    def __init__(self, dbData=None):
        self.datas = []
                        
        #GCP Data
        self.gcPickleName = 'cryptdata'
        self.rawData = None
        
        if dbData:
            self.datas = dbData 
        else: 
            self.loadData()

    def isDataExists(self, cd=crypts.CryptsData()):
        for each in self.datas:
            if each.symbol == cd.symbol and each.entrydate == cd.entrydate and each.entrytime == cd.entrytime:
                tls.debug(f'{cd.symbol} exists in {cd.entrydate}-{cd.entrytime} collection list!')
                return 1
        tls.debug(f'{cd.symbol} not exists in {cd.entrydate}-{cd.entrytime} collection list!')
        return 0
                    
    def addData(self, cd=crypts.CryptsData()):
        info = ''
        if not self.isDataExists(cd):
            self.datas.append(cd)
            info = f'{cd.symbol} added to {cd.entrydate}-{cd.entrytime}!'
        else:
            info = f'{cd.symbol} already exists in {cd.entrydate}-{cd.entrytime}!'
        tls.debug(info)

    def removeData(self, cd=crypts.CryptsData()):
        info = ''
        if self.isExists(cd):
            for each in self.datas:
                if each.symbol == cd.symbol and each.entrydate == cd.entrydate and each.entrytime == cd.entrytime:
                    self.datas.remove(each)
                    info = f'{cd.symbol} removed from {cd.entrydate}-{cd.entrytime}!'
            else:
                if not info: info = f'{cd.symbol} not found in {cd.entrydate}-{cd.entrytime}!'
        else:
            if not info: info = f'{cd.symbol} not available in {cd.entrydate}-{cd.entrytime}!'
        tls.debug(info)
                    
    def loadData(self):
        '''
        Processed Data
        '''
        gc = gcp.GCPSupport()
        raw = gc.readPickle(self.gcPickleName)
        if raw:
            self.datas = raw.datas
        else:
            tls.error(f'GCP Fetch data {self.gcPickleName}')
            self.datas = []
        return self.datas
    
    def storeData(self):
        '''
        Processed Data
        '''
        gc = gcp.GCPSupport()
        res = gc.writePickle(self, self.gcPickleName)
        if res:
            tls.info(f'GCP Data stored {self.gcPickleName}')
        else:
            tls.error(f'GCP Storing data {self.gcPickleName}')
        return res        
        
class CryptEntryStore():
    
    def __init__(self,dbData=None):
        self.datas = []
                        
        #GCP Data
        self.gcPickleName = 'crypttracker'
        self.rawData = None
        
        if dbData:
            self.datas = dbData 
        else: 
            self.loadData()

    def isDataExists(self, cd=crypts.CryptsEntry()):
        for each in self.datas:
            if each.symbol == cd.symbol and each.entrydate == cd.entrydate and each.entrytime == cd.entrytime:
                tls.debug(f'{cd.symbol} exists in {cd.entrydate}-{cd.entrytime} collection list!')
                return 1
        tls.debug(f'{cd.symbol} not exists in {cd.entrydate}-{cd.entrytime} collection list!')
        return 0
                    
    def addData(self, cd=crypts.CryptsEntry()):
        info = ''
        if not self.isDataExists(cd):
            self.datas.append(cd)
            info = f'{cd.symbol} added to {cd.entrydate}-{cd.entrytime}!'
        else:
            info = f'{cd.symbol} already exists in {cd.entrydate}-{cd.entrytime}!'
        tls.debug(info)

    def removeData(self, cd=crypts.CryptsEntry()):
        info = ''
        if self.isExists(cd):
            for each in self.datas:
                if each.symbol == cd.symbol and each.entrydate == cd.entrydate and each.entrytime == cd.entrytime:
                    self.datas.remove(each)
                    info = f'{cd.symbol} removed from {cd.entrydate}-{cd.entrytime}!'
            else:
                if not info: info = f'{cd.symbol} not found in {cd.entrydate}-{cd.entrytime}!'
        else:
            if not info: info = f'{cd.symbol} not available in {cd.entrydate}-{cd.entrytime}!'
        tls.debug(info)
                    
    def loadData(self):
        '''
        Processed Data
        '''
        gc = gcp.GCPSupport()
        raw = gc.readPickle(self.gcPickleName)
        if raw:
            self.datas = raw.datas
        else:
            tls.error(f'GCP Fetch data {self.gcPickleName}')
            self.datas = []
        return self.datas
    
    def storeData(self):
        '''
        Processed Data
        '''
        gc = gcp.GCPSupport()
        data = gc.writePickle(self, self.gcPickleName)
        if data:
            tls.info(f'GCP Data stored {self.gcPickleName}')
        else:
            tls.error(f'GCP Storing data {self.gcPickleName}')
        return data        
      
if __name__ == '__main__':
    tls.info('Start')
    c = CryptDataStore()
    
    c.loadData()
    
    for each in c.datas:
        print(each.symbol, each.entrydate, each.entrytime)
    
    cd=crypts.CryptsData()
    cd.symbol='TEST'
    cd.entrydate='33/33/33'    
    c.addData(cd)
    
    c.gcPickleName = c.gcPickleName + '_test'
    
    #c.storeData() 
    
    tls.info('End')
    
     
