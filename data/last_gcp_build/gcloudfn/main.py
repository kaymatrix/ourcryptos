'''
Created on 18-Apr-2022

#https://kaymatrix.cloudfunctions.net/ctrackfn?do=test
#https://asia-south1-kaymatrix.cloudfunctions.net/ctrack?do=test
https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=test
https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=fetch&view=1
https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=fetch&view=1
https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=verify&view=1


@author: kayma
'''
from lib.cryptlibs import actions
import functions_framework

@functions_framework.http
def ctrackfn(request):
    """
    """
    request_json = request.get_json(silent=True)
    request_args = request.args
    
    cobj = actions.CryptActions()
    
    resp={}
    resp['status']='active'
    
    if request_json and 'do' in request_json:
        todo = request_json['do']
    elif request_args and 'do' in request_args:
        todo = request_args['do']
    else:
        todo = ''
        
    if request_json and 'view' in request_json:
        view = request_json['view']
        view = int(view)
    elif request_args and 'view' in request_args:
        view = request_args['view']
        view = int(view)
    else:
        view = 0
    
    storeToDB = not view
    if todo == 'test': resp = cobj.helloworld()
    if todo == 'fetch': resp = cobj.getLatestData(fetchGeneralData=1, fetchValidCoins=1, alert=1, storeToDB=storeToDB)
    if todo == 'verify': resp = cobj.checkEntries(alert=1, storeToDB=storeToDB)
       
    return resp
