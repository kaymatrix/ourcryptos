'''
Created on 28-May-2022

@author: kayma
'''
from lib import xtools
tls = xtools.getGlobalTools()
from poc.roughtodo import quick
quick.someAction("data")
tls.tags.append('second')


for each in tls.tags:
    tls.info(each)
