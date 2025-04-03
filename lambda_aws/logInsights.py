import boto3,json
import os
import boto3
from datetime import datetime, timedelta
import time

class LogInsightsDishPlus:
    def getAmazonProviderLogs(idSiebel,time,kind,isSpecificSearch):
        specificSearch = ""
        if(isSpecificSearch == True):
            specificSearch = """ and (@message like /(?)conexi/ or @message like /(?)ctualiza/ or @message like /(?)reci/ or @message like /rogramaci/ or @message like /(?)ecarga/)"""
        log_query = '''fields @message 
                    | filter @message like /"{0}"/ and @message like /actionCode/{1} and @message like /REQUEST/ 
                    | sort @timestamp desc | limit 2'''.format(idSiebel,specificSearch)
        log_group = '/aws/lambda/gdev_providerAmazon_prod'
    
        if(kind == "days"):
            log_time = timedelta(days=time)
        else:
            log_time = timedelta(weeks=time)

        return getLog(log_group,log_time,log_query)
    
    def getBodyToResend(logs,newDate,newActionTarget):
        result = None
        try:
            for log in logs:
                #el result de amazonLogs trae un arreglo de esto
                #log trae => {'field': '@message', 'value': '[INFO] 2024-12-13 17:23:22,588 e914ff3f-2ee0-4da0-af9e-1eacb67497ab lambda_function.py:10 lambda_handler() *******REQUEST*******{"providerData": [{"newSerialNumber": "", "previousSerialNumber": "", "provisioningId": "Amazon Prime", "description": "BUNDLE AMAZON PRIME", "dueDate": "12/25/2024 00:00:00", "serviceType": "AMAZON", "actionCode": "RESUME", "type": "Streaming", "technology": "", "unit": "1", "unitType": "", "iccid": "", "msisdn": "", "unitOfMeasure": "", "duration": "", "imsi": "", "unitPrice": "", "netPrice": "", "model": "", "mainServiceType": "SERVICIOS DIGITALES", "equipmentTechnology": null, "id": "1-KJ8X3E2", "idParent": "1-KJ8X3DV", "descriptionParent": "My Services"}], "suscriptorData": {"suscriptorNumber": "6003748", "postalCode": "97302", "status": "Activo", "paymentMethod": "Efectivo", "latitude": "21.091286", "longitude": "-89.666004", "street": "45 B", "email": "malo68bmw@gmail.com", "numeroCelular": "5565189898", "celulares": {"principal": null, "verificado": null}, "folio": "", "tid": "2902039696377", "billCycle": "22", "name": "MARIA ARACELI TREJO NAJAR"}, "orderData": {"orderNumber": "1-44699484747", "employeeNumber": "", "orderType": "Reconexi\\u00f3n", "orderSubType": "Reconexi\\u00f3n autom\\u00e1tica", "orderPaymentType": ""}, "origin": "OPPROVDD", "transactionId": "4014671290"}\n'}
                indexStr = log[0]["value"].find("{")
                jsonReaded = json.loads( log[0]["value"][indexStr:] )

                if('providerData' in jsonReaded):
                    if(newActionTarget == "ADD"):
                        jsonReaded["origin"]= "SOFT_APROV_MVSHUB"
                        
                    if(len(jsonReaded["providerData"])==1):
                        if(newActionTarget != None and newActionTarget != ""):
                            jsonReaded["providerData"][0]["actionCode"] = newActionTarget
                        if(newDate != None and newDate != ""):
                            jsonReaded["providerData"][0]["dueDate"] = newDate.strftime("%m/%d/%Y %H:%M:%S")
                        
                        result = jsonReaded
                        break
                    else:
                        counter = 0
                        for k in jsonReaded["providerData"]:
                            if(counter > 0):
                                jsonReaded["providerData"].remove(k)
                            counter += 1
                        if(newActionTarget != None and newActionTarget != ""):
                            jsonReaded["providerData"][0]["actionCode"] = newActionTarget
                        if(newDate != None and newDate != ""):
                            jsonReaded["providerData"][0]["dueDate"] = newDate.strftime("%m/%d/%Y %H:%M:%S")
                        
                        result = jsonReaded
                        #result = "ERROR_READING_BODY_TWICE_FIELD {0}".format(str(jsonReaded))
                        break
                else:
                    esult = "ERROR_NO_PROVIDER_DATA"

        except Exception as exc:
            print("exc:::::::::::::::::::::::".format(exc))
            return "ERROR_READING_BODY"
    
        return result
    
def getLog(logGroup,logTime,query):
    client = boto3.client('logs')
    
    try:
        start_query_response = client.start_query(
            logGroupName=logGroup,
            startTime=int((datetime.today() - logTime).timestamp()),
            endTime=int(datetime.now().timestamp()),
            queryString=query,
        )
        query_id = start_query_response['queryId']
        response = None

        while response == None or response['status'] == 'Running':
            print('Finding for log...')
            time.sleep(1)
            response = client.get_query_results(
                queryId=query_id
            )
        return response["results"]
        #se devuelve objeto results tipo [ [{ "field": "@message",value:"aaa"},{ "field": "@ptr","value":"bbbb"}], [..],[....],[........]]
        
    except Exception as exc:
        return exc
    
    #fields @timestamp, @message, @logStream, @log
    #| filter @message like /"9171943"/ and @message like /actionCode/ and (@message like /(?)reci/ or @message like /(?)reco/) and @message like /REQUEST/
    #| sort @timestamp desc
    #| limit 1000
