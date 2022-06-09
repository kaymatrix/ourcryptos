'''
Created on 01-Jun-2022
ALL RELATED TO GCP
@author: kayma
'''

import os
import pickle
from google.cloud import storage

from lib.cryptlibs import datastores
from lib import xtools
tls = xtools.getGlobalTools()
    
class GCPSupport():
    
    def __init__(self):    
        self.gcpproject = 'kaymatrix'                  
        self.gcpbucket = 'kaymatrixbucket' 
        if tls.isWindows() and tls.isLocalDev():
            self.gcpkeyfile = 'G:/pythonworkspace/ourcryptos/data/gcp.json' 
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.gcpkeyfile
        
        self.forceGCP = 0        
        self.sc = storage.Client()  
        
    def readPickle(self, pickleName, gcpbucket=None):
        forceGCP = tls.getGlobalSwitch('forceGCP', 0)
        gcpbucket = gcpbucket if gcpbucket else self.gcpbucket
        data = None
        try:
            tls.info(f'GCP: Reading GCP {pickleName}...')
            #InMemoryCheck:
            if tls.isGlobalVarExist(pickleName):
                data = tls.getGlobalVar(pickleName)
                tls.debug(f'GCP: Pickle read {pickleName} from in memory.')
            else:
            #InFileCheck:
                if tls.isLocalDev() and tls.isCacheAvailable(pickleName, dated=1) and not forceGCP: 
                    data = tls.getCache(pickleName, None, dated=1)
                    tls.debug(f'GCP: Pickle read {pickleName} from local')
                else:
                    bucket = self.sc.bucket(gcpbucket)
                    blob = bucket.blob(pickleName)
                    picks = blob.download_as_string()
                    data = pickle.loads(picks)                
                    tls.debug(f'GCP: Pickle read {pickleName}')
                    if tls.isLocalDev(): tls.setCache(pickleName, data, dated=1)
                tls.setGlobalVar(pickleName, data)
        except Exception as e:
            tls.error(f'GCP Error reading the bucket/pickle: {gcpbucket} or {pickleName} - {e}')
        return data

    def writePickle(self, data, pickleName, gcpbucket=None):
        gcpbucket = gcpbucket if gcpbucket else self.gcpbucket
        try:
            tls.info(f'GCP: Storeing GCP {pickleName}...')
            bucket = self.sc.bucket(gcpbucket)
            blob = bucket.blob(pickleName)
            picks = pickle.dumps(data)
            blob.upload_from_string(picks)
            if tls.isLocalDev(): tls.setCache(pickleName, data, dated=1)      
            tls.debug(f'GCP: Pickle written {pickleName}')            
        except Exception as e:
            tls.error(f'GCP Error: writing the bucket/pickle: {gcpbucket} or {pickleName} - {e}')
            return 0
        return 1
    
    def cacheIsExist(self, cacheName, gcpbucket=None):
        gcpbucket = gcpbucket if gcpbucket else self.gcpbucket
        data = None
        try:
            if tls.isLocalDev() and not self.forceGCP:
                return tls.isCacheAvailable(cacheName, dated=1)
            else:
                bucket = self.sc.bucket(gcpbucket)
                blob = bucket.blob(cacheName)
                return 1 if blob else 0
        except:
            tls.error(f'GCP Error reading the bucket/cache: {gcpbucket} or {cacheName}')
        return data

    def cacheRead(self, cacheName, gcpbucket=None):
        gcpbucket = gcpbucket if gcpbucket else self.gcpbucket
        data = None
        try:
            bucket = self.sc.bucket(gcpbucket)
            blob = bucket.blob(cacheName)
            picks = blob.download_as_string()
            data = pickle.loads(picks)
            tls.debug(f'GCP: cache read {cacheName}')
        except:
            tls.error(f'GCP Error reading the bucket/cache: {gcpbucket} or {cacheName}')
        return data     

    def cacheWrite(self, data, cacheName, gcpbucket=None):
        gcpbucket = gcpbucket if gcpbucket else self.gcpbucket
        try:
            bucket = self.sc.bucket(gcpbucket)
            blob = bucket.blob(cacheName)
            picks = pickle.dumps(data)
            blob.upload_from_string(picks)             
            tls.debug(f'GCP: cache written {cacheName}')            
        except:
            tls.error(f'GCP Error: writing the bucket/cache: {gcpbucket} or {cacheName}')
            return 0
        return 1         




        
        
        
if __name__ == '__main__':
    tls.setDebugging()
    
    ds = datastores.CryptDataStore()
    
    g = GCPSupport()

    '''
    
    dbfile = open('20220601ctracker', 'rb')
    rawdata = pickle.load(dbfile)               
    dbfile.close()
    '''
    
    '''
{   'entrydate': '2022-05-24',
    'entryprice': 2.429,
    'exitdate': '',
    'percentchange': -7.67108416,
    'status': 'fail',
    'symbol': 'KDA',
    'targetprice': 2.50187}    
    '''
    '''
    for each in rawdata:
        dt = each
        info = rawdata[each]
        #tls.prittyPrint(info)
        
        cd = crypts.CryptsEntry()
        
        cd.symbol = info['symbol']
        cd.entrydate = dt.split('_')[0]
        cd.entrytime = dt.split('_')[1]        
        cd.entryprice = info['entryprice']
        
        cd.percentage_change = info['percentchange']
        cd.status = info['status']
        cd.targetprice = info['targetprice']
        cd.exitdate = info['exitdate']
        cd.invested = None
        cd.invested_status = None
        
        ds.addData(cd)
    '''

    
    #g.writePickle(ds, 'crypttracker')
    
    
    ds = g.readPickle('cryptdata')    
    #ds = g.readPickle('crypttracker')
    
    for each in ds.datas:
        print(each.symbol, each.entrydate, each.entrytime, each.status)
    
  
    tls.info('End')                