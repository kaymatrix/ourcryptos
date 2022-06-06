'''
Created on 09-Sep-2021

@author: kayma
'''

from lib.cryptlibs import crypts
from lib.cryptlibs import datastores
from lib.cryptlibs import exchanges
from lib.cryptlibs import rules
from lib import gcp 
from lib import xtools
tls = xtools.getGlobalTools()


class CryptDataSupport():
    
    def __init__(self, dbData=None):
        self.tls = tls
        self.bn = exchanges.Binance()
        self.gio = exchanges.Giottus()
        self.wx = exchanges.Wazrix()
        self.gn= exchanges.General()
        self.cmc = exchanges.CoinMarketCap()
        self.crp = exchanges.CryptoPanic() 
        self.gcps = gcp.GCPSupport()
        self.ds = datastores.CryptDataStore(dbData)
        
        self.cmc.getCloudCacheExistsFn = self.gcps.cacheIsExist
        self.cmc.getCloudCacheReadFn = self.gcps.cacheRead
        self.cmc.getCloudCacheWriteFn = self.gcps.cacheWrite
        
        self.today = tls.getDateTime('%Y-%m-%d')
        self.nowtime = tls.getDateTime('%H:%M:%S')
        self.datestamp = tls.getDateTime('%Y-%m-%d %H:%M:%S %p')
        
        self.currentToppers = []
        self.coinInfoAllDetail = True
        
        self.filterPercentageChangeAbove = None
        self.filterPercentageChangeBelow = None
        
        self.dbData = self.ds.datas
    
    def getDBData(self):
        return self.dbData
    
    def getCDForCoin(self, coin, inputList=None):
        workOnList = self._getListToWorkOn(inputList)

        for each in workOnList:
            if each.symbol == coin:
                return coin
        return None        
            
    def getLiveToppers(self):
        '''
        Top losers and Top gainers with other detail
        ('GMT', 29.14275799, 4953394151.036736, 13.37, 5, 20, 20)
        symbol, 24hpercentchnage, 24hvolume, 24hbinancevolumepercent, user_reactions, thisweek_news_cnt, last2days_news_cnt
        
        '''
        tls.info('Fetching latest toppers for now...')
        
        #Topgainer
        tg = self.cmc.getTopGainer()
        
        #Toploser
        tl = self.cmc.getTopLoser()
        
        toppers = tg + tl
        tls.info(f'Found {len(toppers)} toppers symbols, {len(tg)} Gainer and {len(tl)} Losers!')
        
        #Volumepercent
        vp = self.cmc.getMarketVolumeToper()
        today = tls.getDateTime('%Y%m%d')
        tm = 'm' if tls.isItMorning() else 'e'
        
        def marketvoltopper(coin):
            for each in vp:
                if str(each[1]).upper() == str(coin).upper():
                    return str(each[3])
            return 0
        
        def isPercFilterOK(percentageChange):       
            #Filter symbols with specified percentage change only.
            if self.filterPercentageChangeAbove or self.filterPercentageChangeBelow: 
                if (self.filterPercentageChangeAbove and self.filterPercentageChangeBelow):
                    if self.filterPercentageChangeBelow > percentageChange > self.filterPercentageChangeAbove:
                        return 1
                    else:
                        return 0
                elif self.filterPercentageChangeAbove:
                    if (percentageChange > self.filterPercentageChangeAbove):
                        return 1
                    else:
                        return 0
                elif self.filterPercentageChangeBelow:
                    if (percentageChange < self.filterPercentageChangeBelow):
                        return 1
                    else:
                        return 0
                else:
                    return 1
            else:
                return 1             
        
        if self.coinInfoAllDetail:
            tls.info(f'Requested: Coin Details!')
        else:
            tls.info(f'No Request: For Coin Details!')
            
        if not (self.filterPercentageChangeBelow or self.filterPercentageChangeAbove):
            tls.info(f'No Request: For Percentage filter!')
        else:
            tls.info(f'Requested: Percentage filter!')
                    
        resp = []            
        for cnt, each in enumerate(toppers):
            #Basic Info
            #[id,rank,symbol,change,price,vol,slug]            
            symbol = each[2]
            perchg = each[3]                    #%%%
            price =  each[4] 
            ttlvols = each[5]
            binvol = marketvoltopper(symbol)    #%%%
            binvol = float(binvol)
            slug = each[6]
            
            #Detail Info
            #Additional Details need to go more urls                       
            pricechange24h = 0
            low24h = 0
            high24h = 0
            volume24h = 0
            marketcap = 0
            marketdominance = 0
            marketrank = 0                
                          
            usr_react = 0
            usr_weekcnt = 0
            usr_last2dayscnt = 0              
            
            if isPercFilterOK(perchg) and self.coinInfoAllDetail:
                tls.debug(f'Reading {cnt+1}/{len(toppers)} - {symbol} coin info...')
                _pop1 = self.cmc.getCoinInfo(symbol, slug)
                _pop2 = self.crp.getCoinInfo(symbol)

                slug = _pop1['slug']
                price = _pop1['price']
                
                pricechange24h = _pop1['pricechange24h']
                low24h = _pop1['low24h']
                high24h = _pop1['high24h']
                volume24h = _pop1['volume24h']
                marketcap = _pop1['marketcap']
                marketdominance = _pop1['marketdominance']
                marketrank = _pop1['marketrank']                
                
                usr_react = _pop2['ttlall']
                usr_weekcnt = _pop2['weekcnt']
                usr_last2dayscnt = _pop2['last2dayscnt']
            else:
                tls.debug(f'Skipped fetching info for {symbol}...')
             
            # (today, tm, symbol, slug, price, pricechange24h, low24h, high24h, perchg, volume24h, ttlvols, binvol, marketrank, marketcap, marketdominance, usr_react, usr_weekcnt, usr_last2dayscnt)

            # ('20220602', 'e', 'ICP', 'internet-computer', 8.11, 42490.53, 7.49, 8.41, 0.56039756, 1241585703017.26, 124823691.43747047, 0.16, 33, 0.06535, 0.15, 12, 18, 4)
            # ('20220602', 'e', 'FEI', 'fei-usd', 0.9939, 21150.21, 0.9859, 0.994, 0.12943425, 76968369948.8, 7696365.21373755, 0.0, 93, 0.01822, 0.03, 0, 0, 0)
            # ('20220602', 'e', 'USDP', 'paxos-standard', 1.0, 19510.2, 0.9944, 1.0, 0.11710001, 163461451942.98, 16417511.56156502, 0.0, 59, 0.01728, 0.08, 1, 0, 0)
            # ('20220602', 'e', 'DAI', 'multi-collateral-dai', 1.0, 25560.03, 0.9981, 1.0, 0.01535513, 2771192005351.6, 277232058.277573, 0.0, 14, 0.04076, 0.55, 0, 20, 12)
            # ('20220602', 'e', 'USDC', 'usd-coin', 1.0, 22320.02, 0.9997, 1.0, 0.014318, 62232797107915.1, 6236344319.940671, 1.9, 4, 0.115, 4.34, 294, 10, 1)
            # ('20220602', 'e', 'COMP', 'compound', 58.49, None, 56.5, 69.52, -11.61266997, 119947272928.53, 119998818.46682322, 0.0, 94, 0.2877, 0.03, 0, 11, 6)
            
            if isPercFilterOK(perchg):
                cd = crypts.CryptsData()
                cd.symbol = symbol
                cd.slug = slug
                cd.entrydate = today
                cd.entrytime = tm
                
                cd.price = price   
                cd.percentage_change = perchg
                cd.high24h = high24h
                cd.low24h = low24h
                
                cd.volume24h = volume24h
                cd.binvolume = binvol
                cd.ttlvolume = ttlvols
                cd.marketdom = marketdominance
                cd.marketrank = marketrank
                cd.marketcap = marketcap 
                
                cd.usr_last2dayscnt = usr_last2dayscnt
                cd.usr_react = usr_react
                cd.usr_weekcnt = usr_weekcnt

                resp.append(cd)
                self.currentToppers = resp
              
        return resp
                
    #Top Gainers
    def filterByPlusPercentage(self, inputList=None):
        workOnList = self._getListToWorkOn(inputList)
            
        lst = []
        for each in workOnList:
            if each.percentage_change > 0:
                lst.append(each)
        return lst

    #Top Losers
    def filterByNegativePercentage(self, inputList=None):
        workOnList = self._getListToWorkOn(inputList)
            
        lst = []
        for each in workOnList:
            if each.percentage_change < 0:
                lst.append(each)
        return lst
    
    def filterByDateTime(self, date, time=None, inputList=None):
        workOnList = self._getListToWorkOn(inputList)
            
        lst = []
        for each in workOnList:
            if not time and each.entrydate == date:
                lst.append(each)
            elif time and each.entrytime == time and each.entrydate == date:
                lst.append(each)
        return lst
        
    def filterIsContinuingDirectionSinceLastEntry(self, cd, inputList=None):
        workOnList = self._getListToWorkOn(inputList)
        if tls.isItMorning():
            wantDate = tls.getDateCalc(-1,'%Y%m%d') #Yesterday -1
            wantTime = 'e'
        else:
            wantDate = tls.getDateCalc(0,'%Y%m%d') #Today 0        
            wantTime = 'm'
        
        workOnList = self.filterByDateTime(wantDate, wantTime, workOnList)
        for each in workOnList:
            if cd.symbol == each.symbol and cd.entrydate == each.entrydate and cd.entrytime == each.entrytime:
                return True
        return False

    def filterIsItAvailableRecently(self, cd, recentNoOfDays=2, inputList=None):
        workOnList = self._getListToWorkOn(inputList)
        
        newWorkOnList = []
        for e in range(recentNoOfDays, 0 , -1):
            chkForDate = tls.getDateCalc(e * -1,'%Y%m%d')
            tmp = self.filterByDateTime(chkForDate, inputList = workOnList)
            newWorkOnList = newWorkOnList + tmp

        for each in newWorkOnList:
            if cd.symbol == each.symbol:
                return True
        return False

    def _getListToWorkOn(self, inputList=None):
        if inputList:
            workOnList = inputList
        else: 
            if not self.currentToppers: self.getLiveToppers()
            workOnList = self.currentToppers
        return workOnList        
        
class CryptEntrySupport():
    
    def __init__(self):
        self.tls = tls
        self.bn = exchanges.Binance()
        self.gio = exchanges.Giottus()
        self.wx = exchanges.Wazrix()
        self.gn= exchanges.General()
        self.cmc = exchanges.CoinMarketCap()
        self.crp = exchanges.CryptoPanic() 
        self.gcps = gcp.GCPSupport()
        self.des = datastores.CryptEntryStore()
        self.rule = rules.CryptRule_Quick3Percent()
        
        self.today = tls.getDateTime('%Y-%m-%d')
        self.nowtime = tls.getDateTime('%H:%M:%S')
        self.datestamp = tls.getDateTime('%Y-%m-%d %H:%M:%S %p')
        
        self.currentToppersCD = []
        self.currentToppersCE = []
        
        self.coinInfoAllDetail = True
        self.filterPercentageChangeAbove = None
        self.filterPercentageChangeBelow = None        
        
        self.dbEntryData = self.des.datas
        self.dbData = self.rule.cds.dbData
    
    def getCDForCoin(self, coin, inputList=None):
        workOnList = self._getListToWorkOn(inputList)
        for each in workOnList:
            if each.symbol == coin:
                return coin
        return None        
            
    def getLiveEntries(self, maximumEntries=3, allLiveToppers=None):
        '''
        
        '''
        tls.info('Fetching live entries...')
        
        if allLiveToppers:
            toppers = allLiveToppers
        else:
            cds = CryptDataSupport(self.dbData)
            cds.coinInfoAllDetail = self.coinInfoAllDetail
            cds.filterPercentageChangeAbove = self.rule.entryPercent
            cds.filterPercentageChangeBelow = self.rule.entryPercent+4
            toppers = cds.getLiveToppers()
        
        cnt = 1
        self.currentToppersCD = []
        eachTopper = crypts.CryptsData()
        for eachTopper in toppers:
            if cnt<=maximumEntries:
                if self.rule.isSymbolOKToBuy(eachTopper):
                    ce = crypts.CryptsEntry()
                    ce.symbol = eachTopper.symbol
                    ce.entrydate = eachTopper.entrydate
                    ce.entrytime = eachTopper.entrytime
                    ce.entryprice = eachTopper.price
                    ce.percent_change = eachTopper.percentage_change
                    ce.exitdate = ''#tls.getDateCalc(self.rule.waitDuration, '%Y%m%d')
                    ce.targetprice = self._getTargetPrice(ce.entryprice,self.rule.exitPercent) 
                    ce.status = 'waiting'            
                    ce.invest_status = None
                    ce.invested = 0
                    self.currentToppersCD.append(eachTopper)
                    self.currentToppersCE.append(ce)
                    cnt += 1
        return (self.currentToppersCE, self.currentToppersCD)

    def _getTargetPrice(self, currentPrice, exitPercent):
        return float(currentPrice + (tls.getFloat((exitPercent / 100)) * currentPrice)) 

    def _getListToWorkOn(self, inputList=None):
        if inputList:
            workOnList = inputList
        else: 
            if not self.currentToppers: self.getLiveToppers()
            workOnList = self.currentToppers
        return workOnList        
    
if __name__ == '__main__':
    #tls.setDebugging()
    
    obj = CryptEntrySupport()
    data = obj.getLiveEntries()
    ces, cds = data
    
    for each in ces:
        tls.info(each.entrydate, each.entrytime, each.symbol, each.entryprice, each.targetprice, each.status)
    