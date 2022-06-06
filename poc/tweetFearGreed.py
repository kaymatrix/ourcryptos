'''
Created on 17-May-2022

@author: kayma
'''
apikey = 'nIwelYBfBnyGu28l4zpDT9P3G'
apikeysecret = 'spLEwRlZS5YxQMZjcDe5iMMwiMoTCmZjqnJyEP1Y1kBxPOYViL'
bearertoken = 'AAAAAAAAAAAAAAAAAAAAAEzGcgEAAAAAyemmcnT6dTDB48KnvbO4wb47qkY%3DnsYZlELMOVWaKsUTkJOrUgBWOa2O6YooORHsmA1oIeAv9C0N9I'

accesstoken = '1136767650111971329-Elzpa1L5lv5iskLAsbmzqFQoI8d49j'
accesstokensecret = 'fx3Gulv7cB48w7npUDPmO3vpco4cm5IYGlxA37jzH5ueh'

user = '@BitcoinFear'


from twitter import *

t = Twitter(auth=OAuth(accesstoken, accesstokensecret, apikey, apikeysecret))

d = t.statuses.user_timeline(screen_name=user)
print(len(d))
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
        data = (dt, int(val), matter)
        print(data)


