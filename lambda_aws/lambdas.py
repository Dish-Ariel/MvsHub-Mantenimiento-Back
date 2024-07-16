import boto3,json
import os

class LambdaDishPlus:
    def deleteSuscriberSes(id_customer,email):
        try:
            payload = {
                "id_customer": id_customer,
                "email": email
            }
            lambda_client = boto3.client('lambda',region_name="us-east-1")
            lambda_url = os.environ.get("LAMBDA_DELETE_SES")
            response_json = lambda_client.invoke(FunctionName = lambda_url, InvocationType = "RequestResponse",Payload = json.dumps(payload))
            response = json.loads(response_json['Payload'].read())
            return response
            
        except Exception as exc:
            return exc

    def deleteSuscriber(email):
            
        try:
            payload = {
                "method": "Post",
                "sourceIP": os.environ.get("SOURCE"),
                "body": {
                        "email": email
                }
            }
            lambda_client = boto3.client('lambda',region_name="us-east-1")
            lambda_url = os.environ.get("LAMBDA_DELETE_SUSCRIBER")
            response_json = lambda_client.invoke(FunctionName = lambda_url, InvocationType = "RequestResponse",Payload = json.dumps(payload))
            response = json.loads(response_json['Payload'].read())
            return response
            
        except Exception as exc:
            return exc
    
    def deleteDevices(id_customer):
        try:
            payload = {
                "url": os.environ.get("URL_DEVICES_SES").format(id_customer = id_customer),
                "method": "GET"
            }
            lambda_client = boto3.client('lambda',region_name="us-east-1")
            lambda_url = os.environ.get("UNIVERSAL_REQUEST")
            response_json = lambda_client.invoke(FunctionName = lambda_url, InvocationType = "RequestResponse",Payload = json.dumps(payload))
            response = json.loads(response_json['Payload'].read())
            if response:
                        if "deviceDTOList" in response and response["deviceDTOList"]:
                            payload = {
                                "url": os.environ.get("DELETE_DEVICES"),
                                "request": {
                                    "reqIds": [reqId["deviceId"] for reqId in response["deviceDTOList"]]
                                },
                                "method": "POST"
                            }
                            lambda_client = boto3.client('lambda',region_name="us-east-1")
                            lambda_url = os.environ.get("UNIVERSAL_REQUEST")
                            response_json = lambda_client.invoke(FunctionName = lambda_url, InvocationType = "RequestResponse",Payload = json.dumps(payload))
                            response = json.loads(response_json['Payload'].read())
                            return response
        except Exception as e:
            return [e]
