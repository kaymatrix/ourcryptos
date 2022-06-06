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


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?symbol=dcr'
url = 'https://coinmarketcap.com/currencies/bitcoin/'
url = 'https://coinmarketcap.com/currencies/apecoin-ape/'
from bs4 import BeautifulSoup

import requests

'''
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find('tbody')
rows = results.find_all("tr")

price=0
low24h=0
high24h=0
marketdom=0
for each in rows:
    print(each.text)

'''

page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")
results = soup.find('table')
rows = results.find_all("tr")

price=0
low24h=0
high24h=0
marketdom=0
for each in rows:
    print(each.text)




'''
results = soup.find('tbody')
#print(results.prettify())
rows = results.find_all("span")
for each in rows:
    print(each.text)
    #r = each.find_all('td')
    #print(r[0].text, r[2].text, r[7].text)

Price Change24h
24h
-$0.000002685
99.16%

Trading Volume24h
24h
$120,368.55
252829.25%

'''




    