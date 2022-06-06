'''
Created on 05-Jun-2022

@author: kayma
'''
import os
os.environ['gmail_user'] = 'heyp---@gmail.com'
os.environ['gmail_pass'] = '---'

from lib.cryptlibs import datastores
from lib.cryptlibs import exchanges
from lib.cryptlibs import support
from lib.cryptlibs import actions
from lib.cryptlibs import rules
from lib import gcp 
from lib import xtools
tls = xtools.getGlobalTools()
tls.setDebugging()

ca = actions.CryptActions()
ca.checkEntries()