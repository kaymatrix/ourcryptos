'''
Created on 28-May-2022

@author: kayma
'''
from lib import xtools
tls = xtools.getGlobalTools()
tls.tags.append('first')

import pickle

f = open('cache_20220602_cmc-slug','rb')
data = pickle.load(f)
f.close()

# for each in data:
#     tls.info(each)
# tls.info(len(data))

import os

for each in os.environ:
    print(each)
        
if tls.isLocalDev():
    print('ok')