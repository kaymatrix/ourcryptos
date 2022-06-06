'''
Created on 18-Apr-2022

#https://kaymatrix.cloudfunctions.net/ctrackfn?do=test
#https://asia-south1-kaymatrix.cloudfunctions.net/ctrack?do=test
https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=test
https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=fetch&view=1
https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=fetch&view=1
https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=verify&view=1


    
Name    Region    State    Description    Frequency    Target    Last run    Last run result    Next run    Actions
EveningRun    asia-south1    Enabled    Evening 6.30pm    30 18 * * * (Asia/Calcutta)    URL : https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=fetch&view=0    5 Jun 2022, 08:40:07    Has not run yet.    5 Jun 2022, 18:30:00        
Every3MinRun    asia-south1    Enabled    Every 3 min    */3 * * * * (Asia/Calcutta)    URL : https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=verify&view=0    5 Jun 2022, 17:15:00    Success    5 Jun 2022, 17:18:00        
MorningRun    asia-south1    Enabled    Morning 8.30am    30 8 * * * (Asia/Calcutta)    URL : https://ctrackfn-yotxvoz5rq-el.a.run.app/?do=fetch&view=0        Has not run yet.    6 Jun 2022, 08:30:00        

    
Environment    Name    Region    Trigger    Runtime    Memory allocated    Executed function    Last deployed    Authentication    Actions
2nd gen    ctrackfn    asia-south1    HTTP    Python 3.9    256 MiB    ctrackfn    5 Jun 2022, 17:14:59    Allow unauthenticated        

General information
Last deployed
5 June 2022 at 17:16:00 GMT+5
Region
asia-south1
Memory allocated
256 MiB
Timeout
120 seconds
Minimum instances
0
Maximum instances
1000
Service account
kumarglobal@kaymatrix.iam.gserviceaccount.com
Build worker pools
—
Container build log
e103ba65-d406-426b-9d41-76254f486ae6


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
