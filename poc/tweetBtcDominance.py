'''
Created on 17-May-2022

@author: kayma
44.88% Fri May 20 08:00:03 +0000 2022

'''
apikey = 'nIwelYBfBnyGu28l4zpDT9P3G'
apikeysecret = 'spLEwRlZS5YxQMZjcDe5iMMwiMoTCmZjqnJyEP1Y1kBxPOYViL'
bearertoken = 'AAAAAAAAAAAAAAAAAAAAAEzGcgEAAAAAyemmcnT6dTDB48KnvbO4wb47qkY%3DnsYZlELMOVWaKsUTkJOrUgBWOa2O6YooORHsmA1oIeAv9C0N9I'

accesstoken = '1136767650111971329-Elzpa1L5lv5iskLAsbmzqFQoI8d49j'
accesstokensecret = 'fx3Gulv7cB48w7npUDPmO3vpco4cm5IYGlxA37jzH5ueh'

user = '@btcdominance'


from twitter import *

t = Twitter(auth=OAuth(accesstoken, accesstokensecret, apikey, apikeysecret))

d = t.statuses.user_timeline(screen_name=user)

whn = d[0]['created_at']
txt = d[0]['text']
txt = txt.replace('Current BTC Dominance: ', '')
txt = txt.replace(' #Bitcoin #Altcoin #Cryptocurrency','')
print(txt, whn)
