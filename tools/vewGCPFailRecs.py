'''
Created on 13-May-2022

READ GCP DATAS

@author: kayma
'''


from lib import tools
from lib.cryptlibs import GCP_DATA_LIB as gdl
tls = tools.getGlobalTools()

fraw = gdl.getItemsByStatus('fail')
f = gdl.getCurrentStatus(fraw)

fraw = len(fraw)
f = len(f)
print(f'Raw fail: {fraw}')
print(f'Total fail: {f}')

