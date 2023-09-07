import requests
import json
import os

class Requester:
    def PostUniversalRequestPackages(id):
        response = PostUniversalRequest(id)
        array = []
        if response.json() != None:
            if response.json().get("subscribeService") != None:
                array = response.json()["subscribeService"]  
        return array
    
    def PostUniversalRequestUser(id):
        response = PostUniversalRequest(id)
        array = []
        if response.json() != None:
            if response.json().get("remoteSchedulerCustomer") != None:
                array.append(response.json()["remoteSchedulerCustomer"])
        return array
    
    def UpdateUniversalRequestEmail(id,newEmail):
        response = UpdateUniversalRequest(id,newEmail)
        array = []
        #if response.json() != None:
        #    if response.json().get("response") != None:
        #        if response.json().get("response") == id:
        #            array.append(response.json())
        array.append(response)
        return array
    
    def CancelationNetflix(idClienteSiebel):
        response = CancelationNetflix(idClienteSiebel)
        array = []
        array.append(response)
        return array

  
def PostUniversalRequest(id):
    url = os.getenv('REQUEST_UNIVERSALREQUEST_URL')
    myobj = {
        "url":os.getenv('POST_UNIVERSAL_REQUEST'),
        "request":{
            "customerId":id
        },
        "method":"POST"
    }
    response = requests.post(url, json = myobj)
    return response

def UpdateUniversalRequest(id,email):
    url = os.getenv('REQUEST_UNIVERSALREQUEST_URL')
    myobj = {
        "url":os.getenv('UPDATE_UNIVERSAL_REQUEST')+str(id),
        "request": {
            "customerInfo":{
                "email":email
            },
            "remoteSchedulerCustomer":{
                "email": email
            }
        },
        "method":"PUT"
    }
    response = requests.post(url, json = myobj)
    return response.json

def CancelationNetflix(suscriber):
    url = os.getenv('REQUEST_CANCELNETFLIX_URL')
    url_token = os.getenv('REQUEST_CANCELNETFLIX_LOGIN')
    payload_token = { "user":os.getenv('REQUEST_CANCELNETFLIX_USER'), "password":os.getenv('REQUEST_CANCELNETFLIX_PASS') }

    respWs = requests.post(url_token, data = json.dumps(payload_token))
    json_respWs = respWs.json()
    token = json_respWs['netflix']['openid']
    
    
    payload = {
        "suscriptor": suscriber,
        "razonCancelacion": "CANCELACION"
    }
    headers = {"Content-Type": "application/json", "openid": token} 
    response = requests.post(url, data = json.dumps(payload), headers = headers)

    return response.json