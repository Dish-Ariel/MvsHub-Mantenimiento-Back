import boto3,json
import os

class CognitoDishPlus:
    def getSuscriberCognitoByEmail(email):
        client = boto3.client('cognito-idp')
        response = client.list_users(
            UserPoolId = os.getenv('AWSCLI_COGNITO_USERPOOL'),
            Filter = 'email=\"' + email + '\"'
        )
        return response["Users"]
    
    def updateSuscriberEmailCognito(username,newEmail):
        client = boto3.client('cognito-idp')
        response = client.admin_update_user_attributes(
            UserPoolId = os.getenv('AWSCLI_COGNITO_USERPOOL'),
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': newEmail
                }
            ]
        )
        
        return response
    
    def deleteSuscriberSes(id_customer,email):
        
        try:
            payload = {
                "id_customer": id_customer,
                "email": email
            }
            lambda_client = boto3.client('lambda',region_name=os.environ.getenv("REGION_NAME"))
            lambda_url = os.environ.getenv("LAMBDA_DELETE_SES")
            response_json = lambda_client.invoke(FunctionName = lambda_url, InvocationType = "RequestResponse",Payload = json.dumps(payload))
            response = json.loads(response_json['Payload'].read())
            return response
        
        except Exception as exc:
            return exc

    def deleteSuscriber(email):
        
        try:
            payload = {
                "method": "Post",
                "sourceIP": os.environ.getenv("SOURCE"),
                "body": {
                        "email": email
                }
            }
            lambda_client = boto3.client('lambda',region_name=os.environ.getenv("REGION_NAME"))
            lambda_url = os.environ.getenv("LAMBDA_DELETE_SUSCRIBER")
            response_json = lambda_client.invoke(FunctionName = lambda_url, InvocationType = "RequestResponse",Payload = json.dumps(payload))
            response = json.loads(response_json['Payload'].read())
            return response
        
        except Exception as exc:
            return exc

