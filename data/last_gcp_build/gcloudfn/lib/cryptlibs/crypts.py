'''
Created on 26-May-2022

@author: kayma
'''
from lib import xtools
tls = xtools.getGlobalTools()

class CryptsEntry(object):
    '''
        {'entrydate': '2022-05-26', 'percentchange': -8.42745569, 'symbol': 'ETC', 'status': 'waiting', 'targetprice': 23.8342, 'exitdate': '', 'entryprice': 23.14}
        
        status
            waiting
            pass
            fail
            delayed    (delayed pass)
            
        
        investStatus
            waiting
            pass
            manualexit            
            manualgain
            manualloss
        
        
    entrytime     m/e
    m - morning - 8.45
    e - evening - 6.00
    
    '''
    symbol = None
    entrydate = None
    entrytime = None
    entryprice = None
    percent_change = None
    status = None
    targetprice = None
    exitdate = None
    invested = None
    invest_status = None
       
    
class CryptsData(object):
    '''
            # binvolume    float: 0.16    
            # entrydate    str: 20220602    
            # entrytime    str: e    
            # high24h    float: 202.98    
            # low24h    float: 192.59    
            # marketcap    float: 0.06572    
            # marketdom    float: 0.29    %
            # marketrank    int: 24    
            # percentage_change    float: 1.74844219    
            # price    float: 199.42    
            # slug    str: monero    
            # symbol    str: XMR    
            # ttlvolume    float: 237424187.1252744    
            # usr_last2dayscnt    int: 4    
            # usr_react    int: 72    
            # usr_weekcnt    int: 8    
            # volume24h    float: 2376030914814.81    
    
        binvol: 13.27
        (number)
        perchg: 22.92984914
        (number)
        symbol: "GMT"
        (string)
        ttlvols: 4833761413.000184
        (number)
        usr_last2dayscnt: 18
        (number)
        usr_react: 5
        (number)
        usr_weekcnt: 20
        
        'high24h': '1.51',
        'low24h': '1.24',
        'marketcap': '0.6606',
        'marketdominance': '0.13%',
        'marketrank': '39',
        'price': '1.33',
        'pricechange24h': '0.080136.40%',
        'slug': 'the-sandbox',
        'symbol': 'sand',
        'volume24h': '1,080,051,302.00230.21%'
        
    symbol = None
    entrydate = None
    entrytime = m / e        
        
        entrytime     m/e
        m - morning - 8.45
        e - evening - 6.00
        
        (today, tm, symbol, slug, price, pricechange24h, low24h, high24h, perchg, volume24h, ttlvols, binvol, marketrank, marketcap, marketdominance, usr_react, usr_weekcnt, usr_last2dayscnt)
        
cd.symbol =
cd.slug =
cd.entrydate =
cd.entrytime =

cd.price =    
cd.percentage_change =
cd.high24h =
cd.low24h =

cd.volume24h =
cd.binvolume =
cd.ttlvolume =
cd.marketdom =
cd.marketrank =   
cd.marketcap =    

cd.usr_last2dayscnt =
cd.usr_react =
cd.usr_weekcnt =        
            
    '''
    symbol = None
    slug = None
    entrydate = None
    entrytime = None
    
    price = None    #
    percentage_change = None
    high24h = None
    low24h = None
    
    volume24h = None
    binvolume = None
    ttlvolume = None
    marketdom = None
    marketrank = None   #
    marketcap = None    #

    usr_last2dayscnt = None
    usr_react = None
    usr_weekcnt = None

