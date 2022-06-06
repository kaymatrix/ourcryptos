'''
Created on 18-Apr-2022

@author: kayma
'''
from lib.cryptolibs import trackers
import functions_framework

@functions_framework.http
def hello_http(request):
    """
    
     do
     find - find symbols and enter
     track - track status of the symbols added
     
     update
     1
     0 
     
     notify
     1
     0
     
    """
    request_json = request.get_json(silent=True)
    request_args = request.args
    
    resp={}
    resp['status']='active'
    if request_json and 'do' in request_json:
        todo = request_json['do']
    elif request_args and 'do' in request_args:
        todo = request_args['do']
    else:
        todo = ''
    
    if request_json and 'update' in request_json:
        update = request_json['update']
    elif request_args and 'update' in request_args:
        update = request_args['update']
    else:
        update = 0
        
    if request_json and 'notify' in request_json:
        notify = request_json['notify']
    elif request_args and 'notify' in request_args:
        notify = request_args['notify']
    else:
        notify = 0       

    if request_json and 'get' in request_json:
        get = request_json['get']
    elif request_args and 'get' in request_args:
        get = request_args['get']
    else:
        get = 0       

    if todo == 'find': resp = trackers.storeToppers(update)
    if todo == 'find': resp = trackers.storeCurrentRates(update)
    if todo == 'find': resp = trackers.findSymbol(notify, update)
    if todo == 'track': resp = trackers.trackStatus(notify, update)
       
    return resp
