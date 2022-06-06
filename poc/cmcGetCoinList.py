'''
Created on 21-Mar-2022

@author: kayma

ApeCoin Price$8.00
Price Change24h$0.18372.35%
24h Low / 24h High$7.47 /$8.35
Trading Volume24h$662,045,836.471.75%
Volume / Market Cap0.2832
Market Dominance0.18%
Market Rank#32


'''
import codecs
codecs.register_error("strict", codecs.ignore_errors)

apikey = 'd8e96fef-e457-4816-91ed-1c9301cf4dae'

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?symbol=dcr'
url = 'https://weissratings.com/en/crypto/coins'
url = 'https://coinmarketcap.com/currencies/apecoin-ape/'
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'

import requests
import json
import unicodedata

myheaders = {"X-CMC_PRO_API_KEY":apikey}
page = requests.get(url,headers=myheaders)
data = page.content
dj = json.loads(data.decode('utf-8',errors='ignore'))
'''
{'id': 4566, 'name': 'DigitalBits', 'symbol': 'XDB', 'slug': 'digitalbits', 'rank': 169, 'is_active': 1, 'first_historical_data': '2019-09-13T04:29:11.000Z', 'last_historical_data': '2022-05-20T08:59:00.000Z', 'platform': {'id': 1, 'name': 'Ethereum', 'symbol': 'XDB', 'slug': 'digitalbits', 'token_address': '0xb9eefc4b0d472a44be93970254df4f4016569d27'}}
{'id': 4568, 'name': 'JFIN', 'symbol': 'JFC', 'slug': 'jfin', 'rank': 3383, 'is_active': 1, 'first_historical_data': '2021-01-12T11:20:00.000Z', 'last_historical_data': '2022-05-20T08:55:00.000Z', 'platform': {'id': 1, 'name': 'Ethereum', 'symbol': 'JFC', 'slug': 'jfin', 'token_address': '0x940bdcb99a0ee5fb008a606778ae87ed9789f257'}}

'''
lst = []
for each in dj['data']:
    symbol = str(unicodedata.normalize('NFKD', each['symbol']).encode('ascii', 'ignore')) 
    symbol = symbol[2:len(symbol)-1]
    slug = str(unicodedata.normalize('NFKD', each['slug']).encode('ascii', 'ignore'))
    slug = slug[2:len(slug)-1]
    print(symbol, '---',slug)
    lst.append((symbol, slug))

print(lst)
    