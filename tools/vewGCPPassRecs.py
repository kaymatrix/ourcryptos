'''
Created on 13-May-2022

READ GCP DATAS

@author: kayma
'''

from lib import tools
from lib.cryptlibs import GCP_DATA_LIB as gdl
tls = tools.getGlobalTools()

w = gdl.getItemsByStatus('pass')
w= len(w)
print(f'Pass: {w}')

