'''
Created on 21-Mar-2022

[2022-05-20T08:33:39] tron (ftx -> -) : 500000 USD
[2022-05-20T08:33:03] tron (- -> -) : 800000 USD
[2022-05-20T08:32:53] eth (- -> ftx) : 6821081 USD
[2022-05-20T08:32:39] eth (- -> okex) : 1092427.12780762 USD
[2022-05-20T08:32:22] eth (- -> -) : 10000000 USD
[2022-05-20T08:32:08] dash (- -> -) : 464901 USD
[2022-05-20T08:31:40] eth (- -> -) : 818513.2 USD
[2022-05-20T08:31:40] eth (curve.fi -> -) : 6002568 USD
[2022-05-20T08:31:30] tron (- -> ftx) : 500000 USD
[2022-05-20T08:31:19] eth (- -> -) : 500665.53 USD
[2022-05-20T08:31:19] eth (cryptocom -> -) : 749975 USD
[2022-05-20T08:31:18] tron (- -> -) : 1000000 USD
[2022-05-20T08:30:55] usdc (- -> -) : 709679.56 USD
[2022-05-20T08:30:55] eth (- -> -) : 24999978 USD
[2022-05-20T08:30:55] eth (- -> -) : 1078130.66927734 USD
[2022-05-20T08:30:15] tron (- -> bitfinex) : 943997.5 USD
[2022-05-20T08:30:00] eth (- -> okex) : 742942 USD
[2022-05-20T08:30:00] eth (binance -> binance) : 15015137 USD
[2022-05-20T08:30:00] eth (binance -> binance) : 1040000 USD
[2022-05-20T08:30:00] eth (binance -> binance) : 2200204.8 USD
[2022-05-20T08:30:00] eth (binance -> binance) : 3739694.15675365 USD
[2022-05-20T08:29:59] doge (- -> -) : 690155 USD


@author: kayma
'''
from lib import tools
from lib.cryptlibs import GCP_DATA_LIB as gdl
tls = tools.getGlobalTools()
import datetime

presentDate = datetime.datetime.now()
unix_timestamp = datetime.datetime.timestamp(presentDate)*1000
print(unix_timestamp)

# 1648388243129.7
# 1648388251925.955

d = tls.getUnixTimeStamp(seconds = -3599)
print(d)

timestamp = int(d)
value = datetime.datetime.fromtimestamp(timestamp)
print(f"{value:%Y-%m-%d %H:%M:%S}")

'''
https://docs.clankapp.com/#get-a-specific-transaction


3c13c61d22a41e05a2fcbdbb6378edd5


 https://api.clankapp.com/v2/explorer/tx?s_date=desc&t_blockchain=bitcoin&size=5&api_token=9f72e2bd5cad61ee88566038739b98bc&api_key=<YOURAPIKEY>
 
  https://api.clankapp.com/v2/explorer/tx?s_date=desc&size=5&api_key=3c13c61d22a41e05a2fcbdbb6378edd5
  
'''

#https://api.whale-alert.io/v1/transactions?api_key=APUVCDSpr6DNZZUrEfpPwamIj2zbFyBn&min_value=10000&start=1550237797&cursor=2bc7e46-2bc7e46-5c66c0a7
url = f'https://api.whale-alert.io/v1/transactions?api_key=APUVCDSpr6DNZZUrEfpPwamIj2zbFyBn&min_value=500000&start={timestamp}&currency=btc'
url = f'https://api.whale-alert.io/v1/transactions?api_key=APUVCDSpr6DNZZUrEfpPwamIj2zbFyBn&min_value=500000&start={timestamp}'
url = 'https://api.clankapp.com/v2/explorer/tx?s_date=desc&size=5&api_key=3c13c61d22a41e05a2fcbdbb6378edd5'
url = 'https://api.clankapp.com/v2/explorer/tx?s_date=desc&size=150&api_key=3c13c61d22a41e05a2fcbdbb6378edd5'
#url = 'https://api.whale-alert.io/v1/status?api_key=APUVCDSpr6DNZZUrEfpPwamIj2zbFyBn'
from bs4 import BeautifulSoup

import requests

page = requests.get(url)

#print(page.json())
data = page.json()

def _conv(symbol, bc):
    '''
    symbol = usdt
    bc = ethereum
    
    2022-05-20T07:21:01  ethereum  usdt  transfer  huobi  binance
    2022-05-20T07:20:06  tron  usdt  transfer  unknown wallet  unknown wallet
    '''
    giveBack = symbol
    if giveBack == 'usdt':
        giveBack = bc
        if giveBack == 'ethereum':
            giveBack = 'eth'
    return giveBack

def _conv2(location):
    '''
    location = unknown wallet or multiple addresses 
    
    '''
    giveBack = location
    if giveBack == 'unknown wallet':
        giveBack = '-'
    if giveBack == 'multiple addresses':
        giveBack = 'mulitple'
    return giveBack       
lst = data['data']
for each in lst:
    symbol = _conv(each['symbol'], each['blockchain'])
    date = each['date']
    amount_usd = each['amount_usd']
    transaction_type = each['transaction_type']
    from_owner = _conv2(each['from_owner'])
    to_owner = _conv2(each['to_owner'])
    print(f'[{date}] {symbol} ({from_owner} -> {to_owner}) : {amount_usd} USD')
