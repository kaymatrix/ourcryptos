'''
Created on 21-Mar-2022

@author: kayma
1 ETH/BUSD 4.41%
2 BTC/USDT 13.89%
3 BTC/BUSD 5.56%
4 BUSD/USDT 7.44%
5 LUNA/BUSD 2.24%
6 ETH/USDT 9.02%
7 USDC/USDT 3.77%
8 SOL/USDT 1.78%
9 GMT/USDT 2.36%
10 ETH/BTC 2.85%
11 AVAX/USDT 0.97%
'''

#binacne volume
url = 'https://coinmarketcap.com/exchanges/binance/'
from bs4 import BeautifulSoup

import requests


page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find('tbody')

#print(results.prettify())

rows = results.find_all("tr")

for each in rows:
    r = each.find_all('td')
    print(r[0].text, r[2].text, r[7].text)

    