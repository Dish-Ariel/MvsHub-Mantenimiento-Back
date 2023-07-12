from dto.ResponseDTO import ResponseDTO
from dto.MensajesDTO import MessagesDTO
from utils.validations import SuscriberValidator
from utils.querysDishPlus import QuerierDishPlus
from utils.requests import Requester
from utils.cognitos import CognitoDishPlus

class UsersService:
    def getSuscriber(idOrEmail):
        response = ResponseDTO()

        kindId = SuscriberValidator.whatIsIdUser(idOrEmail)
        if kindId == "error":
            response.description = MessagesDTO.ERROR_INVALID_ID_OR_EMAIL
            return response.getJSON()
        
        suscriber = QuerierDishPlus.getSuscriber(kindId,idOrEmail)
        if suscriber == "none":
            response.code = MessagesDTO.CODE_WARNIG
            response.description = MessagesDTO.ERROR_SUSCRIBER_NOT_FOUNDIN_BD
            return response.getJSON()
        
        logs = QuerierDishPlus.getSuscriberLogs(suscriber[0]["folio"])
        packages = Requester.PostUniversalRequestPackages(suscriber[0]["id_customer"])
        cognitos = CognitoDishPlus.getSuscriberCognitoByEmail(suscriber[0]["email"])
        response.code = MessagesDTO.CODE_OK
        response.description = MessagesDTO.OK_USER_FOUND
        response.data = {"suscriber":suscriber, "packages":packages, "cognitos":cognitos, "logs":logs}
        return response.getJSON()
    
    def updateSuscriberEmail(request):
        response = ResponseDTO()
        #CODE VALIDATION (DATA, EXIST)
        isEmailOrId = SuscriberValidator.whatIsIdUser(request.json["emailOrId"])
        isNewEmail = SuscriberValidator.checkIfIsEmail(request.json["newEmail"])
        if request.json["emailOrId"] == request.json["newEmail"]:
            response.description = MessagesDTO.WARNING_SAME_VALUE
            response.data = {"field":"emailOrId=newEmail"}
            return response.getJSON()

        if isEmailOrId == "error": 
            response.description = MessagesDTO.ERROR_INVALID_ID_OR_EMAIL
            response.data = {"field":"emailOrId"}
            return response.getJSON()
        
        if isNewEmail == False:
            response.description = MessagesDTO.ERROR_INVALID_EMAIL
            response.data = {"field":"newEmail"}
            return response.getJSON()

        actualCount = QuerierDishPlus.getSuscriber(isEmailOrId,request.json["emailOrId"])
        newEmailCount = QuerierDishPlus.getSuscriber("email",request.json["newEmail"])

        if actualCount == "none":
            response.description = MessagesDTO.ERROR_SUSCRIBER_NOT_FOUNDIN_BD
            response.data = {"field":"emailOrId", "emailOrId":request.json["emailOrId"]}
            return response.getJSON()
        if newEmailCount != "none":
            response.description = MessagesDTO.ERROR_EMAIL_ALREADY_EXISTIN_BD
            response.data = {"field":"newEmail", "newEmail":newEmailCount, "actualEmail": actualCount}
            return response.getJSON()
        
        emailOrIdCognitos = CognitoDishPlus.getSuscriberCognitoByEmail(actualCount[0]["email"])
        if len(emailOrIdCognitos) == 0:
            response.description = MessagesDTO.ERROR_EMAIL_NOT_FOUNDIN_COGNITO
            response.data = {"field":"emailOrId", "email":actualCount[0]["email"]}
            return response.getJSON()
        else:
            for i in emailOrIdCognitos[0]["Attributes"]:
                fields = []
                values = []
                if i["Name"] == "name":
                    if str(actualCount[0]["name"]).lower() not in str(i["Value"]).lower():
                        fields.append("name")
                        values.append("bd:" + str(actualCount[0]["name"]).lower() + " (NOT IN) cognito:" + str(i["Value"]).lower())
                    if str(actualCount[0]["surname"]).lower() not in str(i["Value"]).lower():
                        fields.append("surName")
                        values.append("bd:" + str(actualCount[0]["surname"]).lower() + " (NOT IN) cognito:" + str(i["Value"]).lower())
                
                if i["Name"] == "phone_number":
                    if actualCount[0]["mobile"] not in i["Value"]:
                        fields.append("mobile")
                        values.append("bd:" + str(actualCount[0]["mobile"]) + " (NOT IN) cognito:" + str(i["Value"]))
                
                if len(fields)>0:
                    response.code = MessagesDTO.CODE_WARNIG
                    response.description = MessagesDTO.WARNING_NOTMATCH_CONGINTO_DB
                    response.data = {"fields":fields, "values":values, "email":actualCount[0]["email"]}
                    return response.getJSON()

        newEmailCognitos = CognitoDishPlus.getSuscriberCognitoByEmail(request.json["newEmail"])
        if len(newEmailCognitos) != 0:
            response.description = MessagesDTO.ERROR_EMAIL_ALREADY_EXISTIN_COGNITO
            response.data = {"field":"newEmail"}
            return response.getJSON()
                
        #CODE UPDATE (MYSQL, COGNITO)
        updateSuscriberResponse = QuerierDishPlus.updateSuscriber(actualCount[0]["email"],request.json["newEmail"])
        if updateSuscriberResponse != "commited":
            response.description = MessagesDTO.ERROR_UPDATEIN_BD
            response.data = {"mysqlResponse":updateSuscriberResponse}
            return response.getJSON()
        
        updateCognitoResponse = CognitoDishPlus.updateSuscriberEmailCognito(emailOrIdCognitos[0]["Username"],request.json["newEmail"])
        if updateCognitoResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
            response.description = MessagesDTO.ERROR_UPDATEIN_COGNITO
            response.data = {"cognitoResponse":updateCognitoResponse,"mysqlResponse":updateSuscriberResponse}
            return response.getJSON()
        
        userSes = Requester.PostUniversalRequestUser(actualCount[0]["id_customer"])
        updateInSes = []
        if len (userSes) != 0:
            updateInSes = Requester.UpdateUniversalRequestEmail(actualCount[0]["id_customer"],request.json["newEmail"])
        
        response.code = MessagesDTO.CODE_OK
        response.data = {"lastEmail":actualCount[0]["email"], "userSes":len(userSes), "sesResponse":updateInSes, "mysqlResponse":updateSuscriberResponse, "cognitoResponse":updateCognitoResponse}
        response.description = MessagesDTO.OK_USER_UPDATED
        return response.getJSON()
        
    def deleteSuscriber(request):
        response = ResponseDTO()
        #CODE

        isEmailOrId = SuscriberValidator.whatIsIdUser(request.json["emailOrId"])
        if isEmailOrId == "error": 
            response.description = MessagesDTO.ERROR_INVALID_ID_OR_EMAIL
            response.data = {"field":"emailOrId"}
            return response.getJSON()
        
        actualCount = QuerierDishPlus.getSuscriber(isEmailOrId,request.json["emailOrId"])
        if actualCount == "none":
            response.description = MessagesDTO.ERROR_SUSCRIBER_NOT_FOUNDIN_BD
            response.data = {"field":"emailOrId", "emailOrId":request.json["emailOrId"]}
            return response.getJSON()
        
        actualEmailCognitos = CognitoDishPlus.getSuscriberCognitoByEmail(actualCount[0]["email"])
        #actualEmailCognitos = CognitoDishPlus.getSuscriberCognitoByEmail(request.json["emailOrId"])
        if len(actualEmailCognitos) == 0:
            response.description = MessagesDTO.ERROR_EMAIL_NOT_FOUNDIN_COGNITO
            response.data = {"field":"emailOrId"}
            return response.getJSON()

        deleteInCognito = CognitoDishPlus.deleteSuscriberCognitoByEmail(actualEmailCognitos[0]["Username"])
        
        response.code = MessagesDTO.CODE_OK
        response.data = str(deleteInCognito)
        response.description = MessagesDTO.OK_USER_DELETED
        return response.getJSON()