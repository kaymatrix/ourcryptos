'''
Created on 21-Mar-2022

@author: kayma

ORI - Other - Orica Showcase Event 2 - 2022-05-21T00:00:00Z - 2022-05-20T03:31:54Z
GHD - Exchange - MEXC Global Listing - 2022-05-20T00:00:00Z - 2022-05-19T14:43:03Z
ADP - Exchange - BitMart Listing - 2022-05-25T00:00:00Z - 2022-05-19T14:18:05Z
PLCU - Exchange - BitMart Listing - 2022-05-23T00:00:00Z - 2022-05-18T22:32:03Z
VGX - Release - App Update - 2022-05-20T00:00:00Z - 2022-05-18T21:57:21Z
NOMAD - Exchange - BTCEX Listing - 2022-05-20T00:00:00Z - 2022-05-18T21:55:32Z
BIP - Exchange - Minter Lists STEPN - 2022-05-20T00:00:00Z - 2022-05-18T21:34:05Z
ERGOPAD - Other - Ergo-Lend IDO on Ergodex - 2022-05-25T00:00:00Z - 2022-05-18T16:39:31Z

'''

import time
import datetime

from lib import tools
from lib.cryptlibs import GCP_DATA_LIB as gdl
tls = tools.getGlobalTools()

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

import requests
url = "https://developers.coinmarketcal.com/v1/events"
#querystring = {"max":"10","coins":"bitcoin"}
querystring = {"max":"75","page":"1","sortBy":"created_desc", "showViews":"true"}
payload = ""
headers = {
   'x-api-key': "jSf8OdeFuM1MBUIGKhYHuICOcrcfR2GyYgcvQzj0",
   'Accept-Encoding': "deflate, gzip",
   'Accept': "application/json"
}
response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

data = response.json()
if 'body' in data and '_metadata' in data:
    cnt = data['_metadata']['total_count']
    for each in data['body']:
        title = each['title']['en']
        symbol = each['coins'][0]['symbol']
        eventOn = each['date_event']
        informedOn = each['created_date']
        category = each['categories'][0]['name']
        print(f'{symbol} - {category} - {title} - {eventOn} - {informedOn}')
    

