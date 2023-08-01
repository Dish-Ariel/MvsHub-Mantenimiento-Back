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
        "url":"https://10.72.2.46:4446/maui/rest/customer/getCustomer",
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
        "url":"https://10.72.2.46:4446/maui/rest/customer/update/"+str(id),
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