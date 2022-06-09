'''
Created on 03-Jun-2022

@author: kayma
'''
from lib.cryptlibs import crypts
from lib.cryptlibs import support
from lib.cryptlibs import exchanges
from lib import gcp 
from lib import xtools
tls = xtools.getGlobalTools()

class CryptRule_Quick3Percent(object):
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
        self.cds = support.CryptDataSupport()
        
        self.entryPercent = -5
        self.exitPercent = 3         
        self.waitDuration = 5        #In Days
        
        self.rankMin = 5
        self.rankMax = 98
        
        #popularity
        self.userRespondToNews = 0
        self.recentNewsCount = 0
        self.weeklyNewsCount = 2
        
        self.cd = crypts.CryptsData()
    
    def isSymbolOKToBuy(self, cd):
        self.cd = cd
        proceed = True
        
        #isRankFallBetweenMinAndMax
        if proceed:
            if not (self.rankMin <= self.cd.marketrank <= self.rankMax):
                tls.info(f'{self.cd.symbol} rank is not ok : {self.cd.marketrank}')
                proceed = False                
        
        #isEntryPercentageOK
        if proceed:
            if not (self.cd.percent_change <= self.entryPercent):
                tls.info(f'{self.cd.symbol} percentage not ok : {self.cd.percent_change}')
                proceed = False
                
        #must be in binance
        if proceed:
            entryprice = self.bn.getCoinPrice(self.cd.symbol)
            if entryprice<=0:
                tls.info(f'{self.cd.symbol} not in binance : {entryprice}')
                proceed = False                
    
        #isCoinPopular
        if proceed:          
            if not self._isCoinPopular(self.cd.usr_react, self.cd.usr_last2dayscnt, self.cd.usr_weekcnt):
                tls.info(f'{self.cd.symbol} not popular as expected')
                proceed = False
                
        #wasYesterdayOrBeforeGoingUp? Dont buy they, may continue to fall 
        if proceed:        
            if self._wasItRecentlyGoingUp(self.cd):
                tls.info(f'{self.cd.symbol} very recently gone up. This might be fall for that.')
                proceed = False
                        
        #wasItInLostSideLastTime? Dont buy it may continue to fall
        if proceed:        
            if self._wasItInLosingSideSinceLastEntry(self.cd):
                tls.info(f'{self.cd.symbol} was on losing side since last entry, and continuing to loose. Not recommanded!')
                proceed = False            
        
        if proceed:
            tls.info(f'{self.cd.symbol} - looks fine!')
            
        return proceed
            
            
    def _isCoinPopular(self, userReactions = 1, veryRecentNews = 1, weekNews = 1):
        if userReactions >= self.userRespondToNews:
            if veryRecentNews >= self.recentNewsCount:
                if weekNews >= self.weeklyNewsCount:
                    return True
        return False
    
    def _wasItRecentlyGoingUp(self, cd):
        data = self.cds.dbData
        data = self.cds.filterByPlusPercentage(data)
        return self.cds.filterIsItAvailableRecently(cd, recentNoOfDays = 3, inputList = data)
        
    def _wasItInLosingSideSinceLastEntry(self, cd):
        data = self.cds.dbData
        data = self.cds.filterByNegativePercentage(data)
        return self.cds.filterIsContinuingDirectionSinceLastEntry(cd, inputList=data)
        
        
    
    