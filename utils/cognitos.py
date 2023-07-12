import boto3
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
    
    def deleteSuscriberCognitoByEmail(username):
        print(str("UserPoolId = " + os.getenv('AWSCLI_COGNITO_USERPOOL') + ", Username = "+ username))
        client = boto3.client('cognito-idp')
        response = client.admin_delete_user(
            UserPoolId = os.getenv('AWSCLI_COGNITO_USERPOOL'),
            Username = username
        )
        
        return response