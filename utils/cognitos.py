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
    
    def getSuscriberCognitoByUserName(username):
        client = boto3.client('cognito-idp')
        response = client.list_users(
            UserPoolId = os.getenv('AWSCLI_COGNITO_USERPOOL'),
            Filter = 'username=\"' + username + '\"'
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
    
    def disableByUsername(username):
        client = boto3.client('cognito-idp')
        response = client.admin_disable_user(
            UserPoolId = os.getenv('AWSCLI_COGNITO_USERPOOL'),
            Username=username,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': username
                }
            ]
        )
        return response
    
    def markEmailAsValid(email):
        client = boto3.client('cognito-idp', region_name = os.getenv('AWS_REGION'))
        response = client.admin_update_user_attributes(
            UserPoolId=os.getenv('AWSCLI_COGNITO_USERPOOL'),
            Username= email,
            UserAttributes=[
                {
                    'Name': 'email_verified',
                    'Value': 'True'
                },
            ]
        )
        return 
    