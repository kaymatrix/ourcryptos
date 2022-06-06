'''
Created on 18-Apr-2022

@author: kayma
'''
import os
keyfile = 'G:/k5522/data/gcp.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = keyfile

from lib.cryptlibs import trackers
from lib import tools

tls = tools.Tools()
#tls.setDebugging()

todo = 'find'
notify = 0
update = 0

if todo == 'find': resp = trackers.findSymbol(notify, update)
if todo == 'track': resp = trackers.trackStatus(notify, update)
if todo == 'toppergrab': resp = trackers.storeToppers(update)
if todo == 'goldgrab': resp = trackers.storeCurrentRates(update)

for each in resp:
    tls.info(str(each) + '' + str(resp[each]))

tls.info('Done')