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

p = gdl.getSpecificSymbolInfo('xmr', '20220423', 'm')
print(p)

#20220423_m_2 {'symbol': 'XMR', 'entryprice': 264.6, 'percentchange': -7.9891164, 'entrydate': '2022-04-23', 'targetprice': 272.538, 'exitdate': '2022-04-23', 'status': 'pass'}

#recs = getMainDataByTime('')
#print(f'Data Records: {recs}')


#50 - 7 wait, 35 pass, 8 fail
#52 - 40pass 12fail

