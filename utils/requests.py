import requests
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