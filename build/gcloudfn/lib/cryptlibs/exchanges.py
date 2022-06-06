'''
Created on 09-Sep-2021

@author: kayma
'''

from binance import Client
from decimal import Decimal
from decimal import *
getcontext().prec = 5
import requests
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from bs4 import BeautifulSoup
from twitter import Twitter,OAuth
import codecs
codecs.register_error("strict", codecs.ignore_errors)
import unicodedata
from lib import xtools
tls = xtools.getGlobalTools()

class General(object):

    def __init__(self):
        
        self.tls = tls
        self.tls.debug('Initializing {0}'.format(self.__class__.__name__))
        
        #'https://api.wazirx.com/api/v2/market-status'
        self.baseurl = 'https://api.wazirx.com/api/v2/'
        self.diffFor = ['inr','usdt','wrx']
        self.marketPriceCache=None
        
        #Twitter API 
        self.apikey = 'nIwelYBfBnyGu28l4zpDT9P3G'
        self.apikeysecret = 'spLEwRlZS5YxQMZjcDe5iMMwiMoTCmZjqnJyEP1Y1kBxPOYViL'
        self.bearertoken = 'AAAAAAAAAAAAAAAAAAAAAEzGcgEAAAAAyemmcnT6dTDB48KnvbO4wb47qkY%3DnsYZlELMOVWaKsUTkJOrUgBWOa2O6YooORHsmA1oIeAv9C0N9I'
        self.accesstoken = '1136767650111971329-Elzpa1L5lv5iskLAsbmzqFQoI8d49j'
        self.accesstokensecret = 'fx3Gulv7cB48w7npUDPmO3vpco4cm5IYGlxA37jzH5ueh'        

    def getGoldRate(self):
        url = 'https://gadgets360.com/finance/digital-gold-price-in-india'
        page = requests.get(url)
        data = str(page.text)
        search1 = '<span>&#8377; '
        t1 = data.find(search1)
        ndata1 = data[t1:]
        t2 = ndata1.find('/g</span>')
        ndata2 = data[t1+len(search1):t1+22]
        ndata2 = ndata2.replace(',','')
        ndata2 = ndata2.replace('/','')
        return float(ndata2) 
    
    def getBTCDominance(self):
        user = '@btcdominance'
        t = Twitter(auth=OAuth(self.accesstoken, self.accesstokensecret, self.apikey, self.apikeysecret))
        d = t.statuses.user_timeline(screen_name=user)
        whn = d[0]['created_at']
        txt = d[0]['text']
        txt = txt.replace('Current BTC Dominance: ', '')
        txt = txt.replace(' #Bitcoin #Altcoin #Cryptocurrency','')
        txt = txt.replace('%','')
        txt = txt.strip()
        tls.debug(f'BTC Dominance: {txt} on {whn}')
        return float(txt)
    
    def getFearGreedIndex(self):
        '''
        Above 50 means all are buying
        '''
        user = '@BitcoinFear'
        t = Twitter(auth=OAuth(self.accesstoken, self.accesstokensecret, self.apikey, self.apikeysecret))
        d = t.statuses.user_timeline(screen_name=user)
        for each in d:
            if 'Bitcoin Fear and Greed Index is ' in each['text']:
                dt = each['created_at']
                txt = each['text']
                val = txt.replace('Bitcoin Fear and Greed Index is ','')
                val = val[0:2]
                matter = txt.replace('Bitcoin Fear and Greed Index is ','')
                matter = matter[3:]
                matterls = matter.split(' ',1)
                if len(matterls)==2:
                    matterls2=matterls[1]
                    matterls2=matterls2.split('\n')
                    matter = matterls2[0]
                return (dt, int(val), matter)
        return ('',0,'')        


#https://api.coingecko.com/api/v3/exchanges/binance/tickers?depth=cost_to_move_up_usd&order=volume_desc
class Wazrix(object):
    
    
    def __init__(self):
        
        self.tls = xtools.getGlobalTools()
        self.tls.debug('Initializing {0}'.format(self.__class__.__name__))
        
        #'https://api.wazirx.com/api/v2/market-status'
        self.baseurl = 'https://api.wazirx.com/api/v2/'
        self.diffFor = ['inr','usdt','wrx']
        self.marketPriceCache=None
        
    def __del__(self):
        self.marketPriceCache=None

    def _urlCall(self, url, headers={}, params={}):
        session = Session()
        session.headers.update(headers)
        data = ''
        try:
            self.tls.debug('Calling ' + url)
            response = session.get(url, params=params)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)
        return data

    def _composeUrl(self,uri='market-status'):
        return self.baseurl + uri

    def getMarketPrice(self):
        if self.marketPriceCache:
            return self.marketPriceCache
        else:
            url = self._composeUrl('market-status')
            data = self._urlCall(url)   
            self.marketPriceCache = data      
            return self.marketPriceCache
    
    def _coinInfo(self,coinItem):
        sellRate  = coinItem['sell'] #currently selling rate
        buyRate = coinItem['buy'] #currently buying rate
        fee = coinItem['fee']['bid']['maker']
        sellRate = self.tls.precision(sellRate,6) if not '0.00000' in sellRate else Decimal(sellRate)
        buyRate = self.tls.precision(buyRate,6) if not '0.00000' in buyRate else Decimal(buyRate)
        fee = self.tls.precision(fee)
                
        return {'sell':sellRate,'buy':buyRate, 'fee':fee } 
    
    def getCoinInfo(self, forcoin=''):
        data = self.getCoinsInfo(forcoin, multiPair=0, inrMust=0)
        return data[forcoin] if forcoin in data else {}
    
    def getCoinsInfo(self, forcoin='', multiPair=1, inrMust=1):
        coins = {}
        data = self.getMarketPrice()
        markets = data['markets']        
        for eachItem in markets:
            currcoin = eachItem['baseMarket']
            if eachItem['status'] == 'active' and eachItem['type'] == 'SPOT':
                if not currcoin in coins: coins[currcoin] = {}
                pair = eachItem['quoteMarket']
                coins[currcoin][pair] = self._coinInfo(eachItem)

        filterd = {}
        def _filterApply(coin, data):
            filterd[coin] = {}
            filterd[coin] = data
        
        def chkINRMust(coin,data):
            if inrMust:
                if 'inr' in data.keys():
                    _filterApply(coin, data)
            else:
                _filterApply(coin, data)

        def chkFilters(coin, data):
            if multiPair:
                if len(data)>1:
                    chkINRMust(coin,data)
            else:
                chkINRMust(coin,data)
        
        if forcoin:
            data=coins[forcoin]
            chkFilters(forcoin,data)
        else:            
            for coin in coins:
                data=coins[coin]
                chkFilters(coin,data)
                
        return filterd
        
    def getPrice(self, coin, output='inr'):
        rate = 0.0
        data = self.getMarketPrice()
        markets = data['markets']        
        for eachItem in markets:
            if eachItem['baseMarket'] == coin.lower().strip() and eachItem['quoteMarket'] == output and eachItem['status'] == 'active':
                rate = self._coinInfo(eachItem)
                break;
        return rate

class Binance(object):
    '''
    classdocs
    '''

    def __init__(self, api_key='', api_secret=''):
        '''
        Constructor
        '''
        self.tls = xtools.getGlobalTools()
        self.tls.debug('Initializing {0}'.format(self.__class__.__name__))
        
        self.api_key = api_key if api_key else "mFLaEOrGL0d9hE0JsuM6cHFb05kgi5obSCDOgyLJMtsIDyXP4tbm2bNTdgIj95PP"
        self.api_secret = api_secret if api_secret else "vAMWWOiz0DI8WzClw3UTFCQLiBkwABF0Gaa2W4CSBBy9dhvXI6O7lR14lf1a8ucg"
        self.bclient = Client(self.api_key, self.api_secret)
        
        self.pairCoin = 'USDT'
        
    def _urlCall(self, url, headers={}, params={}):
        session = Session()
        session.headers.update(headers)
        data = ''
        try:
            self.tls.debug('Calling ' + url)
            response = session.get(url, params=params)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)
        return data

    def _urlCallPost(self, url, body={}, headers={}, params={}):
        session = Session()
        session.headers.update(headers)
        data = ''
        try:
            self.tls.debug('Calling ' + url)
            response = session.post(url,json=body, params=params)
            print(response.text.encode('UTF-8'))
            data = json.loads(response.text.encode('UTF-8'))
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)
        return data
    
    def getP2PRate(self):
        url = 'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search'
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Content-Length": "500",
            "content-Type": "application/json",
            "Host": "p2p.binance.com",
            "Origin": "https://p2p.binance.com"
        }
        inp = {
          "asset": "USDT",
          "fiat": "INR",
          "merchantCheck": False,
          "page": 1,
          "payTypes": [],
          "publisherType": None,
          "rows": 10,
          "tradeType": "BUY"
        }
        response = requests.post(url, headers=headers, json=inp)
        #print(response.text.encode('UTF-8'))
        resp = json.loads(response.text.encode('UTF-8'))
        data = []
        if resp:
            for each in resp['data']:
                n = each['adv']['price']
                #print(n)                
                n = float(n)
                n = round(n,2)
                data.append(n)
        else:
            data.append(0.0)
        
        ret = 0.0
        takeItem = 5
        if len(data)>=takeItem:
            ret = data[takeItem-1]
        else:
            ret = data[0]
        return ret
    
    def getCoinPrice(self, coin):
        '''
        in usdt
        coin must be in binance (confirm by getting price detail from binance)
        '''
        coin = coin.upper().strip() + self.pairCoin.upper().strip()
        prices = self.bclient.get_all_tickers()
        finprice = ''
        for each in prices:
            name = each['symbol']
            price = each['price']
            if coin == name:
                finprice = price
        if finprice == '':
            self.tls.debug('Requested coin price not found : ' + coin)
            finprice = 0.0
        return Decimal(finprice)
    
    def getTradeFee(self, coin, pairwith='USDT'):
        coin = coin.upper().strip()
        fees = self.bclient.get_trade_fee(symbol=coin)
        if len(fees)>0:        
            return Decimal(fees[0]['takerCommission'])
        else:
            return 0
        
    def getCoinBalance(self, coin):
        data = self.bclient.get_asset_balance(asset=coin)
        free = data['free']
        locked = data['locked']
        if not free.startswith('0.00000'):
            return Decimal(free)
        if not locked.startswith('0.00000'):
            return Decimal(locked)
        return Decimal(0.0)
    
    def previewSell(self, coin):
        currPrice = self.getCoinPrice(coin)
        myBalance = self.getCoinBalance(coin)
        tradeFee = self.getTradeFee(coin)
        bnbBalance = self.getCoinBalance('BNB')
        ttlAmount = currPrice * myBalance
        ttlFee = ttlAmount * (tradeFee/100)
        feetype = 'BNB'
        if bnbBalance < ttlFee:
            ttlAmount = ttlAmount - ttlFee
            feetype = 'USDT'
        data = {}
        data['coin'] = coin
        data['currprice'] = currPrice
        data['mybalance'] = myBalance
        data['total'] = ttlAmount
        data['fee'] = ttlFee
        data['feetype'] = feetype
        return data
    
class CoinStats(object):
    
    def __init__(self):
        '''
        Constructor
        '''
        self.tls = xtools.getGlobalTools()
        self.tls.debug('Initializing {0}'.format(self.__class__.__name__))
        
        self.baseUrl = 'https://api.coinstats.app/public/v1'
        
    def getCoinPriceTicker(self,coin):
        '''
        No garuentee, Limit using this fn
        '''    
        url = self.baseUrl + '/tickers?exchange=Binance&pair='+coin.strip().upper()+'-USDT'
        response = requests.request("GET", url)
        return response.text
    
    def getCoinPrice(self,coin,fiet='INR'):
        '''
        No garuentee, Limit using this fn
        '''
        url = self.baseUrl + '/coins?skip=0&limit=2050&currency='+fiet
        response = requests.request("GET", url)
        data = response.json()
        cnt=1
        for each in data['coins']:
            cnt=cnt+1
            if each['symbol'].strip().upper() == coin.strip().upper():
                return (each['name'],each['symbol'],each['price'])
        return None
            
class CoinMarketCap(object):

    def __init__(self, api_key=''):
        '''
        Constructor
        '''

        self.tls = xtools.getGlobalTools()
        self.tls.debug('Initializing {0}'.format(self.__class__.__name__))
        
        self.baseUrl = 'https://pro-api.coinmarketcap.com/v1'
        self.api_key = api_key if api_key else "d8e96fef-e457-4816-91ed-1c9301cf4dae"
        
        self.getCloudCacheReadFn = None
        self.getCloudCacheWriteFn = None
        self.getCloudCacheExistsFn = None
        
        self.nowSlugs = []
        
    def _urlCallSimple(self, url, params={}):
        '''
        Simple Get Call with API response output
        '''
        #print(url)
        #url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        #print(url)
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }
        session = Session()
        session.headers.update(headers)
        data = ''
        try:
            self.tls.debug('Calling ' + url)
            response = session.get(url, params=params)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)        
        return data
    
    def _urlCall(self, uri='/cryptocurrency/listings/latest', params={}):
        url = self.baseUrl + uri    
        #print(url)
        #url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        #print(url)        
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }
        session = Session()
        session.headers.update(headers)
        data = ''
        try:
            self.tls.debug('Calling ' + url)
            response = session.get(url, params=params)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)        
        return data        

    def getCoinInfo(self, coin, slug=None):
        '''

        The Sandbox Price$1.35
        Price Change24h$0.144912.05%
        24h Low / 24h High$1.20 /$1.38
        Trading Volume24h$1,229,375,862.92225.85%
        Volume / Market Cap0.7432
        Market Dominance0.13%
        Market Rank#39
        
        '''
        coinSlug = slug if slug else self.getCoinSlug(coin)
        if coinSlug == None: return None
        
        murl = f'https://coinmarketcap.com/currencies/{coinSlug}/'
        
        page = requests.get(murl)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find('table')
        rows = results.find_all("tr")

        info = {}
        for each in rows:
            nw = each.text
            
            info['symbol'] = coin
            info['slug'] = coinSlug
            
            if 'Price$' in nw:
                nw = nw.split('Price$')
                nw = nw[1]
                nw = nw.replace('%','')
                nw = nw.replace(',','')                
                nw = nw.replace('.','',nw.count('.')-1)
                if not any(c.isalpha() for c in nw):
                    nw = Decimal(nw)
                    nw = float(nw)                
                    info['price'] = nw
                continue
            
            if 'Price Change24h$' in nw:
                nw = nw.replace('Price Change24h$','')
                nw = nw.replace('%','')
                nw = nw.replace(',','')
                nw = nw.replace('.','',nw.count('.')-1)
                if not any(c.isalpha() for c in nw):
                    nw = Decimal(nw)
                    nw = float(nw)
                    info['pricechange24h'] = nw
                continue
                
            if '24h Low / 24h High$' in nw:
                nw = nw.replace('24h Low / 24h High$','')
                nw = nw.replace(',','')
                nw2 = nw.split(' /$')
                nw = Decimal(nw2[0])
                nw = float(nw2[0])                
                info['low24h'] = nw
                nw = Decimal(nw2[1])
                nw = float(nw2[1])                 
                info['high24h'] = nw
                continue

            if 'Trading Volume24h$' in nw:
                nw = nw.replace('Trading Volume24h$','')
                nw = nw.replace('%','')
                nw = nw.replace(',','')
                nw = nw.replace('.','',nw.count('.')-1)
                if not any(c.isalpha() for c in nw):
                    nw = Decimal(nw)
                    nw = float(nw)                
                    info['volume24h'] = nw
                continue

            if 'Volume / Market Cap' in nw:
                nw = nw.replace('Volume / Market Cap','')
                nw = nw.replace('%','')
                nw = nw.replace(',','')                
                nw = nw.replace('.','',nw.count('.')-1)
                if not any(c.isalpha() for c in nw):
                    nw = Decimal(nw)
                    nw = float(nw)                   
                    info['marketcap'] = nw
                continue

            if 'Market Dominance' in nw:
                nw = nw.replace('Market Dominance','')
                nw = nw.replace('%','')
                nw = nw.replace(',','')
                nw = nw.replace('.','',nw.count('.')-1)
                if not any(c.isalpha() for c in nw):
                    nw = Decimal(nw)
                    nw = float(nw)                   
                    info['marketdominance'] = nw    
                continue  

            if 'Market Rank#' in nw:
                nw = nw.replace('Market Rank#','')
                info['marketrank'] = int(nw)  
                continue                         
        
        if not 'pricechange24h' in info: info['pricechange24h'] = None
        if not 'volume24h' in info: info['volume24h'] = None
        if not 'marketrank' in info: info['marketrank'] = None
        if not 'marketdominance' in info: info['marketdominance'] = None
        if not 'marketcap' in info: info['marketcap'] = None
        if not 'low24h' in info: info['low24h'] = None
        if not 'high24h' in info: info['high24h'] = None
        if not 'price' in info: info['price'] = None
        
        #{'symbol': 'WAVES', 'slug': 'waves', 'price': '9.60', 'pricechange24h': '0.83079.48%', 'low24h': '8.50', 'high24h': '11.28', 'volume24h': '3,227,893,315.5530.35%', 'marketcap': '3.1', 'marketdominance': '0.08%', 'marketrank': '51'}
        return info

    
    def getMarketVolumeToper(self):
        '''
        '''
        murl = 'https://coinmarketcap.com/exchanges/binance/'
        
        page = requests.get(murl)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find('tbody')
        rows = results.find_all("tr")
        datas = []
        for each in rows:
            r = each.find_all('td')
            #1 BTC/USDT 2.70%
            #2 GMT/USDT 1.39%
            #3 ETH/USDT 2.17%            
            rank, pair, price, volpercent = r[0].text, r[2].text, r[3].text, r[7].text
            if '/USDT' in pair:
                volpercent = volpercent.replace('%','')
                price = price.replace('$','').replace(',','')
                pair = pair.replace('/USDT','')
                volpercent = float(volpercent)
                price = float(price)
                datas.append([rank,pair,price,volpercent])
        
        datas.sort(key=lambda row: (row[3],row[0]), reverse=True)
        #dts = pd.DataFrame(datas, columns =['rank', 'pair', 'price', 'volpercent'])        
        #dts = dts.sort_values(by = ['volpercent','rank'], ascending = False)
        #print(dts)
        
        #dx = dts.values.tolist()
        return datas
        
    def quickSort(self, datas, sortby='change', cols=['id','rank','symbol','change','price','vol']):
        inx = 0
        for cnt, each in enumerate(cols):
            if each == sortby:
                inx = cnt
                break
        datas.sort(key=lambda row: (row[inx]), reverse=True)
        #dts = pd.DataFrame(datas, columns = cols)        
        #dts = dts.sort_values(by = [sortby], ascending = True)
        return datas
                    
    def getTopGainer(self,howManyToFetch=30):
        '''
        Top Gainers
        '''
        murl = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/spotlight?dataType=2&limit=[TOFETCH]&rankRange=[RANKRANGE]&timeframe=24h'
        
        toFetch = howManyToFetch
        toFetch = str(toFetch)        
        rankRange = str(100) #60 - 100
        murl = murl.replace('[TOFETCH]',toFetch)
        murl = murl.replace('[RANKRANGE]',rankRange)
        ret = self._urlCallSimple(murl)
        data = []
        if ret:
            lst = ret['data']['gainerList']
            data = self._getGainerLoserInfo(lst)
        return data

    def getTopLoser(self,howManyToFetch=30):
        '''
        Top Gainers
        '''
        murl = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/spotlight?dataType=2&limit=[TOFETCH]&rankRange=[RANKRANGE]&timeframe=24h'
        toFetch = howManyToFetch
        toFetch = str(toFetch) #5 - 30
        rankRange = str(100) #60 - 100
        murl = murl.replace('[TOFETCH]',toFetch)
        murl = murl.replace('[RANKRANGE]',rankRange)
        ret = self._urlCallSimple(murl)        
        data = []
        if ret:  
            lst = ret['data']['loserList']
            data = self._getGainerLoserInfo(lst)
        return data
    
    def _getGainerLoserInfo(self, lst):
        data = []
        for eachItem in lst:
            id = eachItem['id']
            symbol = eachItem['symbol']
            rank = eachItem['rank']
            change = eachItem['priceChange']['priceChange24h']
            price = eachItem['priceChange']['price']
            vol = eachItem['priceChange']['volume24h']  
            slug = eachItem['slug']
            data.append([id,rank,symbol,change,price,vol,slug])
        return data         
    
    def getHistory(self, id):
        '''
        History
        '''    
        #https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=4847&convertId=2796&timeStart=1642032000&timeEnd=1647129600
        
        murl = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical?id=[ID]&timeStart=1642032000&timeEnd=1647129600'
    
    def getCoinPrice(self, coin, fiet='INR'):
        '''
        Limit using this function. Counted using
        '''
        uri = '/mytools/price-conversion'    
        params =  {
                'amount':'1',
                'symbol':coin,
                'convert':fiet
            }
        ret = self._urlCall(uri,params)        
        return ret['data']['quote']['INR']['price']
    

    def getCoinSlug(self, coin):
        '''
        slug is special name in cmc 
        
        used in 
        url = 'https://coinmarketcap.com/currencies/bitcoin/'
        
        exception - ape alone
        url = 'https://coinmarketcap.com/currencies/apecoin-ape/
        '''
        def getSlug(lst, coin):
            for each in lst:
                if each[0].strip().upper() == coin.strip().upper():
                    return each[1]
            return None
        
        if self.nowSlugs:
            lst = self.nowSlugs
        else:
            cacheName = 'cache_slug'
            if tls.isLocalDev():
                if self.tls.isCacheAvailable(cacheName):
                    lst = self.tls.getCache(cacheName)
                else:
                    lst = self._fetchOnlineSlugs()
                    self.tls.setCache(cacheName, lst)
            else:
                if self.getCloudCacheExistsFn and self.getCloudCacheReadFn and self.getCloudCacheWriteFn:
                    if self.getCloudCacheExistsFn(cacheName):
                        lst = self.getCloudCacheReadFn(cacheName)
                    else:
                        lst = self._fetchOnlineSlugs()
                        self.getCloudCacheWriteFn(cacheName, lst)
                else:
                    lst = self._fetchOnlineSlugs()
            self.nowSlugs = lst
            
        return getSlug(lst, coin)
  


    def _fetchOnlineSlugs(self):
        murl = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': self.api_key,
        }
        lst = []        
        session = Session()
        session.headers.update(headers)
        data = ''
        try:
            self.tls.debug('Calling ' + murl)
            response = session.get(murl)
            data = response.text
            dj = json.loads(data)
            for each in dj['data']:
                symbol = str(unicodedata.normalize('NFKD', each['symbol']).encode('ascii', 'ignore')) 
                symbol = symbol[2:len(symbol)-1]
                slug = str(unicodedata.normalize('NFKD', each['slug']).encode('ascii', 'ignore'))
                slug = slug[2:len(slug)-1]
                #print(symbol, '---',slug)
                lst.append((symbol, slug))            
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)
        return lst              
        
    
class Giottus(object):
    
    def __init__(self, api_key=''):
        '''
        Constructor
        '''
        self.tls = xtools.getGlobalTools()
        self.tls.debug('Initializing {0}'.format(self.__class__.__name__))
        
        self.baseUrl = 'https://www.giottus.com/api/ticker'
    
    def _urlCall(self ):
        url = self.baseUrl    
        session = Session()
        data = ''
        try:
            response = session.get(url)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)        
        return data
    
    def getCoinPrice(self, coin, fiet='INR'):
        data = ''
        coin = coin+'/'+fiet
        coin = coin.strip()
        try:
            response = self._urlCall()
            data = response
            prc = data['prices']
            for each in prc:
                if coin == each:
                    return Decimal (prc[each])
                    
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)        
        return data

class CryptoPanic(object):
    
    def __init__(self, api_key=''):
        '''
        Constructor
        '''
        self.tls = xtools.getGlobalTools()
        self.tls.debug('Initializing {0}'.format(self.__class__.__name__))
        
        self.baseUrl = 'https://cryptopanic.com/api/v1/posts/?auth_token=2b6b8188040e2a9e5cea6d13a4a8adde5312df72'
        
    def _urlCall(self,input=''):
        url = self.baseUrl    
        session = Session()
        data = ''
        try:
            self.tls.debug(url+input)
            response = session.get(url+input)
            data = json.loads(response.text)
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)        
        return data
    
    def getCoinInfo(self, coin):
        '''
        bearish, bullish, 
        filter=(rising|hot|bullish|bearish|important|saved|lol)
        
        {'ttlnegative': 0, 'ttlpositive': 2, 'ttlliked': 3, 'ttldisliked': 0, 'ttllol': 0, 'ttlcomments': 0, 'ttlimportant': 0, 'ttlall': 5, 'weekcnt': 20, 'last2dayscnt': 13}
        '''
        res = {}

        input= f'&filter={filter}&currencies={coin}&page=1'
        input= f'&currencies={coin}&page=1'

        try:
            data = self._urlCall(input)
            weekcnt = 0
            last2dayscnt = 0
            if len(data['results'])>0:
                isCoinFound = False
                ttlnegative = 0
                ttlpositive = 0
                ttlliked = 0
                ttldisliked = 0
                ttllol = 0
                ttlimportant = 0
                ttlcomments = 0
                ttlall = 0
                for each in data['results']:
                    currencies = each['currencies']
                    votes = each['votes']
                    negative = votes['negative']
                    positive = votes['positive']
                    liked = votes['liked']
                    disliked = votes['disliked']
                    lol = votes['lol']
                    important = votes['important']
                    comments = votes['comments']
                    date = each['published_at']
                    for eachCur in currencies:
                        inCoin = eachCur['code']
                        if inCoin.upper() == coin.upper():
                            isCoinFound = True
                            ttlnegative += negative
                            ttlpositive += positive
                            ttlliked += liked
                            ttldisliked += disliked
                            ttllol += lol
                            ttlimportant += important
                            ttlcomments += comments  
                            ttlall += negative + positive +  liked + disliked + lol + important + comments
                    date = date.split('T')[0]
                    today = self.tls.getDateCalc(0)
                    diff = self.tls.getDateDiff(today,date)
                    if diff > -7: weekcnt += 1
                    if diff > -2: last2dayscnt += 1
                                    
                if isCoinFound:
                    res['ttlnegative']=ttlnegative
                    res['ttlpositive']=ttlpositive
                    res['ttlliked']=ttlliked
                    res['ttldisliked']=ttldisliked
                    res['ttllol']=ttllol
                    res['ttlcomments']=ttlcomments
                    res['ttlimportant']= ttlimportant   
                    res['ttlall'] = ttlall
                    res['weekcnt'] = weekcnt
                    res['last2dayscnt'] = last2dayscnt         
                    
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            self.tls.error(e)        
        return res

    def isCoinTrendingNow(self, coin, usrActionExpected = 5, veryRecentNews = 5, weekNews = 6):
        data = self.getCoinInfo(coin)
        #{'ttlnegative': 0, 'ttlpositive': 2, 'ttlliked': 3, 'ttldisliked': 0, 'ttllol': 0, 'ttlcomments': 0, 'ttlimportant': 0, 'ttlall': 5, 'weekcnt': 20, 'last2dayscnt': 13}
        self.tls.debug(data)
        if data['ttlall']  >= usrActionExpected:
            if data['last2dayscnt'] >= veryRecentNews:
                if data['weekcnt'] >= weekNews:
                    self.tls.debug(f'Coin {coin} is trending')
                    return True
        self.tls.debug(f'Coin {coin} is not popular now')
        return False
                