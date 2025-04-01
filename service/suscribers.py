from dto.ResponseDTO import ResponseDTO
from dto.MensajesDTO import MessagesDTO
from dao.querysAmazon import QuerierAmazonPrime
from utils.validations import SuscriberValidator
from utils.querysDishPlus import QuerierDishPlus
from utils.querysAprdb import QuerierAprdb
from utils.requests import Requester
from utils.cognitos import CognitoDishPlus
from lambda_aws.logInsights import LogInsightsDishPlus
from lambda_aws.lambdas import LambdaDishPlus
from utils import customLogger
import logging
from datetime import datetime,timedelta
import datetime as datetimer
import json, re
import time

class UsersService:

    def getSuscribersRT(request):
        response = ResponseDTO()

        dateFrom = SuscriberValidator.checkIfIsDate(request.json["dateFrom"])
        dateTo = SuscriberValidator.checkIfIsDate(request.json["dateTo"])
        if dateFrom == False or dateTo == False:
            response.description = MessagesDTO.ERROR_INVALID_DATE
            return response.getJSON()
        
        suscribersRT = QuerierDishPlus.getSuscribersRT(dateFrom,dateTo)
        for suscriber in suscribersRT:
            usersCognito = CognitoDishPlus.getSuscriberCognitoByEmail(suscriber["email"])
            if(len(usersCognito)==1):
                suscriber["IsActive"] = usersCognito[0]["Enabled"]
            elif(len(usersCognito) ==0):
                suscriber["IsActive"] = "X"
            elif(len(usersCognito) >1):
                suscriber["IsActive"] = "X-" + str(len(usersCognito))

        response.code = MessagesDTO.CODE_OK
        response.description = MessagesDTO.OK_USERS_FOUND
        response.data = {"suscribersRT":suscribersRT}
        return response.getJSON()
    
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
        
        #Check in the admin_mvshub_activation_link table, if the account exist, for update it
        existActivationLink = QuerierDishPlus.getEmailActivationLink(actualCount[0]["email"])
        if existActivationLink != "none":
            updateActivationLink = QuerierDishPlus.updateEmailActivationLink(actualCount[0]["email"],request.json["newEmail"])
            if(updateActivationLink != "commited"):
                response.description = MessagesDTO.ERROR_UPDATEIN_BD
                response.data = {"mysqlResponse":updateActivationLink}
                return response.getJSON()

        updateCognitoResponse = CognitoDishPlus.updateSuscriberEmailCognito(emailOrIdCognitos[0]["Username"],request.json["newEmail"])
        if updateCognitoResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
            response.description = MessagesDTO.ERROR_UPDATEIN_COGNITO
            response.data = {"cognitoResponse":updateCognitoResponse,"mysqlResponse":updateSuscriberResponse}
            return response.getJSON()
        
        markCognitoResponse = CognitoDishPlus.markEmailAsValid(request.json["newEmail"])
        if markCognitoResponse['ResponseMetadata']['HTTPStatusCode'] != 200:
            response.description = MessagesDTO.ERROR_MARKINGIN_COGNITO
            response.data = {"cognitoResponse":markCognitoResponse,"mysqlResponse":updateSuscriberResponse}
            return response.getJSON()
        
        userSes = Requester.PostUniversalRequestUser(actualCount[0]["id_customer"])
        updateInSes = []
        if len (userSes) != 0:
            updateInSes = Requester.UpdateUniversalRequestEmail(actualCount[0]["id_customer"],request.json["newEmail"])
            response.description = MessagesDTO.OK_USER_UPDATED_SES(request.json["newEmail"],actualCount[0]["email"])
        else:
            response.description = MessagesDTO.OK_USER_UPDATED(request.json["newEmail"],actualCount[0]["email"])

        response.code = MessagesDTO.CODE_OK
        response.data = {"lastEmail":actualCount[0]["email"], "userSes":len(userSes), "sesResponse":updateInSes, "mysqlResponse":updateSuscriberResponse, "cognitoResponse":updateCognitoResponse, "existActivationLink":existActivationLink}

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
            
        #get the user from cognito using email from db
        actualEmailCognitos = CognitoDishPlus.getSuscriberCognitoByEmail(actualCount[0]["email"])
        if len(actualEmailCognitos) == 0:
            #delete user 
            response.description = MessagesDTO.ERROR_EMAIL_NOT_FOUNDIN_COGNITO
            response.data = {"field":"emailOrId"}
            return response.getJSON()
            #validate user in cognito = user in bd
        else: 
            for i in actualEmailCognitos[0]["Attributes"]:
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
                #update username if not exists
                if i["Name"] == "sub":
                    if actualCount[0]["username"] not in i["Value"]:#Validate if have username in db
                        if QuerierDishPlus.validate_sub(i["Value"]) == "none":#Validate that the username doesn't exist in db
                            status = QuerierDishPlus.update_username(i["Value"], actualCount[0]["email"])
                            if status != "commited":
                                fields.append("update_username_failed")
                                values.append(str(response))
        if request.json["force"] != 'Y':  
            if len(fields)>0:
                response.code = MessagesDTO.CODE_WARNIG
                response.description = MessagesDTO.WARNING_NOTMATCH_CONGINTO_DB
                response.data = {"fields":fields, "values":values, "email":actualCount[0]["email"]}
                return response.getJSON()
            
            #validate payments
            validate_payment = QuerierDishPlus.check_payments(actualCount[0]["id_cliente_siebel"],actualCount[0]["id_cliente"])
            if validate_payment != "none":
                response.description = MessagesDTO.ERROR_USER_HAS_PAYMENTS
                response.data = {"field":validate_payment}
                return response.getJSON()
            
            #validate if data source is telmex or dish with a purchase
            source = ["telmex","pagWebTelmexG3"]
            if (actualCount[0]["source"] in source or (actualCount[0]["source"] == "dish" and actualCount[0]["id_cliente_siebel"] != 0)):
                response.description = MessagesDTO.ERROR_CANNOT_DELETE_ONLY_UPDATE
                response.data = {"source":actualCount[0]["source"], "status":actualCount[0]["status"], "id_cliente_siebel":actualCount[0]["id_cliente_siebel"], "id_customer":actualCount[0]["id_customer"]}
                return response.getJSON()

        #delete from cache_pagos
        delete_cache_pagos = QuerierDishPlus.delete_cache_pagos(actualCount[0]["mobile"],actualCount[0]["id_cliente"],actualCount[0]["id_cliente_siebel"])
        if delete_cache_pagos != "commited" and delete_cache_pagos != "none":
            response.description = MessagesDTO.ERROR_WITH_CONNECTION_DB
            response.data = {"field":delete_cache_pagos}
            return response.getJSON()
            
        # delete from customer_cards_domiciliations
        delete_domiciliations = QuerierDishPlus.delete_domiciliation(actualCount[0]["folio"])
        if delete_domiciliations != "commited" and delete_domiciliations != "none":
            response.description = MessagesDTO.ERROR_WITH_CONNECTION_DB
            response.data = {"field":delete_domiciliations}
            return response.getJSON()

        delete_ventas = QuerierDishPlus.delete_ventas(actualCount[0]["folio"])
        if delete_ventas != "commited" and delete_ventas != "none":
            response.description = MessagesDTO.ERROR_WITH_CONNECTION_DB
            response.data = {"field":delete_ventas}
            return response.getJSON()
                
        # delete from admin_mvshub_activation_link
        delete_admin_mvshub_activation_link = "none"
        existActivationLink = QuerierDishPlus.getEmailActivationLink(actualCount[0]["email"])
        if existActivationLink != "none" and len(existActivationLink) ==1:            
            delete_admin_mvshub_activation_link = QuerierDishPlus.deleteEmailActivationLink(actualCount[0]["email"])
            if delete_admin_mvshub_activation_link != "commited" and delete_admin_mvshub_activation_link != "none":
                response.description = MessagesDTO.ERROR_WITH_CONNECTION_DB
                response.data = {"field":delete_admin_mvshub_activation_link}
                return response.getJSON()
            
        
        #¿USER IN SES?
        userSes = []
        delete_user_SES = []
        delete_devices = []
        delete_from_siebel_pendiente = []
        if actualCount[0]["id_cliente"] != 0:
            userSes = Requester.PostUniversalRequestUser(actualCount[0]["id_cliente"])
            if len (userSes) != 0:
                delete_devices = LambdaDishPlus.deleteDevices(actualCount[0]["id_cliente"])
                delete_user_SES = LambdaDishPlus.deleteSuscriberSes(actualCount[0]["id_cliente"],actualCount[0]["email"])
                #¿LEAD IN SIEBEL?
                if actualCount[0]["dth"] == "NO":
                    delete_from_siebel_pendiente = QuerierDishPlus.delete_from_siebel(actualCount[0]["email"], actualCount[0]["id_customer"])
        detail_customer = QuerierDishPlus.insertDetailCustomer(actualCount)
        #deleteuser
        delete_user = LambdaDishPlus.deleteSuscriber(actualCount[0]["email"])
        #VALIDATE IF LAMBDA DELETED THE CUSTOMER
        if delete_user["status_code"] != 200:
            response.code = MessagesDTO.CODE_ERROR
            response.data = {"Delete_user":actualCount[0]["email"],"deleteuserResponse":delete_user, "userSes":userSes, "sesResponse":delete_user_SES,"devices_deleted":delete_devices,
                        "cachepagosResponse":delete_cache_pagos, "Siebel_pendiente" : delete_from_siebel_pendiente, "cards_domiciliation":delete_domiciliations, "ventas": delete_ventas, "detail_customer":detail_customer}
            response.description = MessagesDTO.ERROR_WITH_LAMBDA
            return response.getJSON()

        

        response.code = MessagesDTO.CODE_OK
        response.data = {"Delete_user":actualCount[0]["email"],"deleteuserResponse":delete_user, "userSes":userSes, "sesResponse":delete_user_SES,"devices_deleted":delete_devices,
                        "cachepagosResponse":delete_cache_pagos, "Siebel_pendiente" : delete_from_siebel_pendiente, "cards_domiciliation":delete_domiciliations, "ventas": delete_ventas, "deleteActivationLink":delete_admin_mvshub_activation_link,"detail_customer":detail_customer}
        response.description = MessagesDTO.OK_USER_DELETED(actualCount[0], userSes)
        return response.getJSON()

    def disableSuscriberRT(request,actions):
        response = ResponseDTO()

        #Get fields of request
        usernameCognito = request.json["usernameCognito"]
        #idSiebel = request.json["idSiebel"]
        #status = request.json["status"]

        #User has permissions? static for now
        if (usernameCognito != None and ("MVSHUB.disableSuscriberRT" in actions)):
            #Get and validate if user exist in cognito
            idClienteSiebel = ""
            sucriberCognito = CognitoDishPlus.getSuscriberCognitoByUserName(usernameCognito)
            if len(sucriberCognito) <= 0:
                response.description = MessagesDTO.ERROR_USERNAME_NOT_FOUNDIN_COGNITO
                return response.getJSON()
            else:
                if(sucriberCognito[0]["Enabled"]==False):
                    response.description = MessagesDTO.ERROR_USERNAME_DISABLED_COGNITO
                    return response.getJSON()

            #Get email from cognito's attributes
            for i in sucriberCognito[0]["Attributes"]:
                email = "none"
                if i["Name"] == "email":
                    email = i["Value"]

            #Get actual acount in bd, and check if exist
            actualCount = QuerierDishPlus.getSuscriber("email",email)
            if actualCount == "none":
                response.description = MessagesDTO.ERROR_SUSCRIBER_NOT_FOUNDIN_BD
                response.data = {"field":"emailFromCognito", "emailFromCognito":email}
                return response.getJSON()
            
            #Get siebel id, and check if is not null or empty
            if(len(actualCount)>0):
                idClienteSiebel = actualCount[0]["id_cliente_siebel"]
                date = ""

                if(idClienteSiebel == None or idClienteSiebel == 0 or idClienteSiebel == ""):
                    response.description = MessagesDTO.ERROR_SUSCRIBER_NOT_FOUNDIN_SBL
                    response.data = {"field":"emailFromCognito", "emailFromCognito":email}
                    return response.getJSON()

            #DO update in tables, when is commited, then disable from cognito by username
            updateSuscriberRTFake = "validations ok" #QuerierAprdb.updateSuscriberRTFake(idClienteSiebel)
            if updateSuscriberRTFake != "commited":
                response.description = MessagesDTO.ERROR_UPDATEIN_BD
                response.data = {"mysqlResponse":updateSuscriberRTFake}
                return response.getJSON()

            suscriberCognitoDisabled = "validations ok"#CognitoDishPlus.disableByUsername(usernameCognito)

        response.code = MessagesDTO.CODE_OK
        response.description = MessagesDTO.OK_USER_DISABLED
        response.data = {"DB":actualCount, "Cognito":suscriberCognitoDisabled, "Bd":updateSuscriberRTFake}
        return response.getJSON()
    
    def disableServicesRT(request,actions):
        response = ResponseDTO()

        #Get fields of request (we will need check if field exist)
        idClienteSiebel = request.json["idClienteSiebel"]
        reason = request.json["reason"]
        ticket = request.json["ticket"]

        #User has permissions? static for now
        if (idClienteSiebel != None and ("MVSHUB.disableServicesRT" in actions)):
            #Get and validate if user till exist in db, for call cancelations... and check if is not added to amazon db
            checkSuscriberRTFake = QuerierAprdb.checkSuscriberRTFake(idClienteSiebel)
            checkSuscriberAmazonDisabled = QuerierDishPlus.check_amazon_prime(idClienteSiebel)
            #Check if suscriber are disabled of table
            if(checkSuscriberRTFake != "none"):
                response.description = MessagesDTO.ERROR_SUSCRIBER_NOT_READYTO_DISABLE
                response.data = {"field":"idClienteSiebel", "idClienteSiebel":idClienteSiebel, "checkSuscriberRTFake":checkSuscriberRTFake,'checkSuscriberAmazonDisabled':checkSuscriberAmazonDisabled}
                return response.getJSON()
            #Check if suscriber is not added to table of amazon
            if(checkSuscriberAmazonDisabled == "none"):
                response.description = MessagesDTO.ERROR_SUSCRIBER_ALREADY_DISABLE_AMAZON
                response.data = {"field":"idClienteSiebel", "idClienteSiebel":idClienteSiebel, "checkSuscriberRTFake":checkSuscriberRTFake,'checkSuscriberAmazonDisabled':checkSuscriberAmazonDisabled}
                return response.getJSON()
            
            #after all validations, CALL service to cancel netflix, and insert value to bd to cancel amazon, for the lambda fuse_CancelacionesAmazon_prod
            messageNetflix = "validations ok" #Requester.CancelationNetflix(idClienteSiebel)
            messageAmazon = "validations ok" #QuerierDishPlus.disable_amazon_prime(idClienteSiebel,reason,ticket)

        response.code = MessagesDTO.CODE_OK
        response.description = MessagesDTO.OK_SUSCRIBER_SERVICES_DISABLED
        response.data = {"serviceNetfix":messageNetflix,"serviceAmazon":messageAmazon}
        return response.getJSON()
    
    def disableAccounts():
        response = ResponseDTO()
        return response.getJSON()
    
    def fixProviderAmazon(request):
        loggerFxAmz = logging.getLogger('amazonPrime')

        response = ResponseDTO()
        client = request.json["idCustomerSes"]
        logWeeks = request.json["logWeeks"]
        isForced = request.json["force"]
        toleranceDays = request.json["toleranceDays"]

        loggerFxAmz.info("*********** entro a:{0} buscar por: {1} semana(s)".format(client,logWeeks))
        response.data["client"] = client
        isEmailOrId = SuscriberValidator.whatIsIdUser(client)
        if isEmailOrId == "error": 
            response.data["result"] = MessagesDTO.ERROR_INVALID_ID_OR_EMAIL
            response.description = "Buen día El suscriptor ingresado es erroneo Saludos"
            return response.getJSON()
        
        #Query for get suscriber data from dishplus
        actualCount = QuerierDishPlus.getSuscriber(isEmailOrId,client)
        loggerFxAmz.info("actualCount:{0} isEmailOrId:{1}".format(str(actualCount),str(isEmailOrId)))
        if actualCount == "none" or actualCount == "error":
            response.data["result"] = "ERROR_SUSCRIBER_NOT_FOUNDIN_DISHPLUS"
            response.description = "Buen día No se puede localizar la cuenta en la bd de dishplus Saludos"
            return response.getJSON()

        #Get suscriber data from amazon
        amazonSuscriber = QuerierAmazonPrime.getSuscriber(actualCount[0]["id_cliente_siebel"])
        loggerFxAmz.info("amazonSuscriber:{0}".format(str(amazonSuscriber)))
        if amazonSuscriber == "none":
            response.data["result"] = "ERROR_SUSCRIBER_NOT_FOUNDIN_AMAZON"
            response.description = "Buen día No se puede localizar la cuenta en la bd de Amazon Saludos"
            return response.getJSON()

        amazonLogsToday = LogInsightsDishPlus.getAmazonProviderLogs(actualCount[0]["id_cliente_siebel"],toleranceDays,"days",False)
        if(len(amazonLogsToday)!=0 and isForced == "N"):
            loggerFxAmz.info("amazonLogsToday:{0}".format(str(amazonLogsToday)))
            #bodySendedToday = LogInsightsDishPlus.getBodyToResend(amazonLogsToday,None,None)
            #loggerFxAmz.info("bodySendedToday:{0}".format( json.dumps(bodySendedToday, separators=(',', ':')) ))
            response.data["result"] = "ERROR_LOGS_EXECUTED_TODAY"
            response.description = "Buen día EL día de hoy hubo una ejecución favor de validar Saludos"
            return response.getJSON()
        
        #Get actual offer from ses (of amazon prime)
        amazonPackage = Requester.PostUniversalRequestPackage(actualCount[0]["id_customer"],["AMAZON PRIME ","PAQUETE ENTRETENIMIENTO"])
        loggerFxAmz.info("amazonPackage:{0}".format(str(amazonPackage)))

        if len (amazonPackage) == 0:
            response.data["result"] = "ERROR_PACKAGE_NOT_FOUNDIN_SES"
            response.description = "Buen día No se ve el paquete amazon en SES Saludos"
            return response.getJSON()
        
        if(amazonPackage[0]["expireDt"] == None):
            response.data["result"] = "ERROR_PACKAGE_NOT_AVALIALBLE_SES"
            response.description = "Buen día No se ve vigencia en el paquete amazon en SES Saludos"
            return response.getJSON()
        else:
            readDate = datetime.strptime(amazonPackage[0]["expireDt"],"%m/%d/%Y")
            #MANUAL
            newDate = readDate + datetimer.timedelta(days=2)

        actionTarget = ""
        if(amazonSuscriber[0]["status"] == "SUBSCRIPTION_TERMINATION_SUCCEEDED"):
            query = "1NSERT INT0 suscriptors (id_cliente,id_customer,id_suscription,id_product,date_suscription,date_update,status,orderNumber) VALUES ({0},'{1}','{2}','{3}','{4}','{5}','{6}','{7}')".format(amazonSuscriber[0]["id_cliente"],amazonSuscriber[0]["id_customer"],amazonSuscriber[0]["id_suscription"],amazonSuscriber[0]["id_product"],amazonSuscriber[0]["date_suscription"],amazonSuscriber[0]["date_update"],amazonSuscriber[0]["status"],amazonSuscriber[0]["orderNumber"])
            loggerFxAmz.info(query)
            actionTarget = "ADD"

        elif (amazonSuscriber[0]["status"] == "SUBSCRIPTION_SUSPENDED"):
            actionTarget = "RESUME"
        else:
            response.data["result"] = "ERROR_SUSCRIBER_STATUS_{0}".format(amazonSuscriber[0]["status"])
            actionTarget = "NONE"
            response.description = "Buen día Favor de validar el estatus de la cuenta, ya que es {0} Saludos".format(amazonSuscriber[0]["status"])
            return response.getJSON()
        
        amazonLogs = LogInsightsDishPlus.getAmazonProviderLogs(actualCount[0]["id_cliente_siebel"],logWeeks,"weeks",True)
        loggerFxAmz.info("amazonLogs:{0}".format(str(amazonLogs)))
        if(len(amazonLogs)==0):
            response.data["result"] = "ERROR_LOGS_NOTFOUND"
            response.description = "Buen día No se ven logs previos de esta cuenta en aws Saludos"
            return response.getJSON()
        
        if(amazonSuscriber[0]["status"] == "SUBSCRIPTION_TERMINATION_SUCCEEDED"):
            deletedAmazon = QuerierAmazonPrime.deleteSuscriber(actualCount[0]["id_cliente_siebel"])
            if(deletedAmazon == "none" or deletedAmazon == "error"):
                response.data["result"] = "ERROR_TO_DELETE_STATUS_{0}".format(deletedAmazon)
                response.description = "Error en bd al eliminar"
                return response.getJSON()
            time.sleep(2)
        
        bodyToSend = LogInsightsDishPlus.getBodyToResend(amazonLogs,newDate,actionTarget)
        loggerFxAmz.info("bodyToSend:{0}".format( json.dumps(bodyToSend, separators=(',', ':')) ))
        
        #SEND the new body to lambda for provide amazon, new date with more thays and action target 
        #MANUAL

        if(actionTarget=="RESUME" or actionTarget == "ADD"):
            lambdaProviderAmazonRes = LambdaDishPlus.sendLambdaFunction("gdev_providerAmazon_prod",bodyToSend,"us-east-1")    
            #loggerFxAmz.info("lambdaProviderAmazonRes:{0}".format( json.dumps(lambdaProviderAmazonRes, separators=(',', ':'))) )
            loggerFxAmz.info("lambdaProviderAmazonRes:{0}".format( str(lambdaProviderAmazonRes) ))
            response.code = MessagesDTO.CODE_OK
            response.data["result"] = "OK {0}".format(actionTarget)
            response.description = "Buen día se reanuda la vigencia solicitada Saludos"
        #else:
        #    response.code = MessagesDTO.CODE_WARNIG
        #    response.data["result"] = json.dumps(bodyToSend, separators=(',', ':'))
        #    response.description = "Borrar en bd de amazon y ejecutar en aws \tBuen día se reanuda la vigencia solicitada Saludos"

        return response.getJSON()
    
    def addProviderAmazon(request):
        response = ResponseDTO()
        data = QuerierDishPlus.getSuscriber("email",request.json["email"])
        duadate = request.json["vigencia"]
        print(data[0]['folio'])
        #Create request for gdev_providerAmazon_prod and send it twice
        with open('constants/templates.json') as file:
            templates = json.load(file)
            validity = str((datetime.now()+timedelta(int(duadate))).strftime('%m/%d/%Y %H:%M:%S'))
            
            if request.json["Action"] == "RESUME":
                templates[0]['providerData'][0]['actionCode'] = "RESUME"
            
            #request for gdev_providerAmazon_prod
            templates[0]['suscriptorData']['suscriptorNumber'] = str(data[0]['id_cliente_siebel']) 
            templates[0]['suscriptorData']['suscriptorNumberSES'] = str(data[0]['id_customer']) 
            templates[0]['suscriptorData']['email'] = str(data[0]['email']) 
            templates[0]['suscriptorData']['numeroCelular'] = str(data[0]['mobile'])
            templates[0]['suscriptorData']['name'] = str(data[0]['name']+" "+data[0]['surname'])
            templates[0]['providerData'][0]['dueDate'] = validity
            
            #request for gdev_consume_provider_dish_digital_prod_TEST
            templates[1]['suscriptorData']['suscriptorNumber'] = str(data[0]['id_cliente_siebel']) 
            templates[1]['suscriptorData']['suscriptorNumberSES'] = str(data[0]['id_customer']) 
            templates[1]['suscriptorData']['email'] = str(data[0]['email']) 
            templates[1]['suscriptorData']['numeroCelular'] = str(data[0]['mobile'])
            templates[1]['suscriptorData']['name'] = str(data[0]['name']+" "+data[0]['surname'])
            templates[1]['providerData'][0]['dueDate'] = validity
            templates[1]['providerData'][1]['dueDate'] = validity
            templates[1]['providerData'][0]['vigencia'] = str(duadate)
            templates[1]['providerData'][1]['vigencia'] = str(duadate)
            
        
        
        request_amazon = templates[0]
        request_dish = templates[1]

        if request.json["Action"] == "RESUME":
            response_amazon_validity = LambdaDishPlus.sendLambdaFunction("gdev_providerAmazon_prod",request_amazon,"us-east-1")
            #Open amazon in ses
            response_dish = LambdaDishPlus.sendLambdaFunction("gdev_consume_provider_dish_digital_prod_TEST",request_dish,"us-east-1")
            response.code = MessagesDTO.CODE_OK
            response.description = "Aprovisionamiento realizado con RESUME"
            response.data = {"response_amazon_validity":response_amazon_validity,"response_dish":response_dish}
            return response.getJSON()

        ##First execution sends email with activation link and the second inserts the customer into the validity table
        response_amazon_email = LambdaDishPlus.sendLambdaFunction("gdev_providerAmazon_prod",request_amazon,"us-east-1")
        response_amazon_validity = LambdaDishPlus.sendLambdaFunction("gdev_providerAmazon_prod",request_amazon,"us-east-1")
        #Open amazon in ses
        response_dish = LambdaDishPlus.sendLambdaFunction("gdev_consume_provider_dish_digital_prod_TEST",request_dish,"us-east-1")
        
        response.code = MessagesDTO.CODE_OK
        response.description = "Aprovisionamiento realizado con ADD"
        response.data = {"response_amazon_email":response_amazon_email,"response_amazon_validity":response_amazon_validity,"response_dish":response_dish}
        return response.getJSON()

