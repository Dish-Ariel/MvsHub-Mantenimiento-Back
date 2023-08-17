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
    
