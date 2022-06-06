'''
Created on 17-Apr-2022

@author: kayma
'''

from lib import tools
from lib.cryptlibs import GCP_DATA_LIB as gdl
from lib.cryptlibs import gainerloser as gl
tls = tools.getGlobalTools()
        
if __name__ == '__main__':
    
    #tls.setDebugging()
    
    rh = gl.RecentHappening()
   
    res = rh.getLosersOn()
    for each in res:
        print(each)
    
    res = rh.isContinueLosing(coin='XMR')
    print(res)
        
print('done')