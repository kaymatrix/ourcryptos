'''
Created on 05-Jun-2022

@author: kayma
'''
import os
os.environ['gmail_user'] = '----@gmail.com'
os.environ['gmail_pass'] = '----'

from lib.cryptlibs import crypts
from lib.cryptlibs import datastores
from lib.cryptlibs import exchanges
from lib.cryptlibs import support
from lib.cryptlibs import actions
from lib.cryptlibs import rules
from lib import gcp 
from lib import xtools
tls = xtools.getGlobalTools()



obj = actions.CryptActions()
obj.helloWorld()
tls.helloWorld()
tls.notify(str(obj.helloWorld()), str(obj.helloWorld()),'hello')