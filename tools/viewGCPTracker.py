'''
Created on 13-May-2022

READ GCP DATAS

@author: kayma
'''

from lib import tools
from lib.cryptlibs import GCP_DATA_LIB as gdl
tls = tools.getGlobalTools()
   

#t1 = getItemByTime('20220509','m')
#t2 = getItemsByStatus('a',t1)

#getItemByTime('','')

p = gdl.getItemsByStatus('pass')
fraw = gdl.getItemsByStatus('fail')
f = gdl.getCurrentStatus(fraw)
w = gdl.getItemsByStatus('waiting')

pcnt = len(p)
fcnt = len(f)

ttl = pcnt + fcnt

for each in p:
    print(each, p[each])
for each in f:
    print(each, f[each])
for each in w:
    print(each, w[each])
        
perc = (pcnt/ttl) * 100
print(f'Success: {perc}%')

#recs = getMainDataByTime('')
#print(f'Data Records: {recs}')



#50 - 7 wait, 35 pass, 8 fail
#52 - 40pass 12fail

