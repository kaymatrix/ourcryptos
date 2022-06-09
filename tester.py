import os,sys
from lib import xtools
tls = xtools.getGlobalTools()

tls.info('')
tls.info('Environment Variables')
tls.info('----------------------------------')
for each in os.environ:
    tls.info((each,os.environ[each]))

tls.info('')
tls.info('Env Path')
tls.info('----------------------------------')
paths = os.environ['PATH']
paths = paths.split(';')
for each in paths:
    tls.info(each)    

tls.info('')
tls.info('Sys Path')
tls.info('----------------------------------')
for each in sys.path:
    tls.info(each)    