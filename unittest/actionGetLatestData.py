'''
Created on 05-Jun-2022

@author: kayma
'''
import os,sys
from lib import xtools
tls = xtools.getGlobalTools()
from lib.cryptlibs import crypts
from lib.cryptlibs import datastores
from lib.cryptlibs import exchanges
from lib.cryptlibs import support
from lib.cryptlibs import actions
from lib.cryptlibs import rules
from lib import gcp 


forceGCP = 0

tls.setDebugging()
tls.setGlobalSwitch('forceGCP', forceGCP)

ca = actions.CryptActions()
fetchGeneralData = 1
fetchValidCoins = 1
alert = 1 
storeToDB = 0

resp = ca.getLatestData(fetchGeneralData, fetchValidCoins, alert, storeToDB)

tls.prittyPrint(resp)