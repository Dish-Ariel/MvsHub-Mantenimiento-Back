from flask import Flask
from flask import request
from dotenv import load_dotenv
from utils import customLogger
from werkzeug.exceptions import HTTPException
from service.suscribers import UsersService
from dto.ResponseDTO import ResponseDTO
import logging

app = Flask(__name__)
load_dotenv()

customLogger.initLogger("amazonPrime")
customLogger.initLogger('activity')
logger = logging.getLogger('activity')

@app.route("/")
def main():
    return "<h1>Api funcionando</h1>"

@app.route("/getSuscribersRT", methods = ['POST'])
def getSuscribersRT():
    actions = ["MVSHUB.getSuscribersRT"]
    return UsersService.getSuscribersRT(request)
    #return {"actionDummy":"Geted"}

@app.route("/getSuscriber/<string:idOrEmail>", methods = ['GET'])
def getSuscriberEmail(idOrEmail):
    return UsersService.getSuscriber(idOrEmail)
    #return {"actionDummy":"Geted"}

@app.route("/updateSuscriberEmail", methods = ['POST'])
def updateSuscriberEmail():
    logger.info("updateSuscriberEmail req=> {0}".format(str(request)))
    response = UsersService.updateSuscriberEmail(request)
    logger.info("updateSuscriberEmail res=> {0}".format(str(response)))
    return response
    #return {"actionDummy":"Updated"}

@app.route("/deleteSuscriberEmail", methods = ['POST'])
def deleteSuscriberEmail():
    logger.info("deleteSuscriberEmail req=> {0}".format(str(request)))
    response = UsersService.deleteSuscriber(request)
    logger.info("deleteSuscriberEmail res=> {0}".format(str(response)))
    return response
    #return {"actionDummy":"deleted"}

@app.route("/disableSuscriberRT", methods = ['POST'])
def disableSuscriberRT():
    actions = ["MVSHUB.disableSuscriberRT","MVSHUB.markSuscriberRT"]
    return UsersService.disableSuscriberRT(request,actions)
    #return {"actionDummy":"deleted"}

@app.route("/disableServicesRT", methods = ['POST'])
def disableServicesRT():
    actions = ["MVSHUB.disableServicesRT"]
    return UsersService.disableServicesRT(request,actions)
    #return {"actionDummy":"deleted"}

@app.route("/disableAccounts",  methods = ['POST'])
def disableAccounts():
    #Agregar la carpeta files/deactivations en el directorio actual para poder procesar este req
    return UsersService.disableAccounts()

@app.route("/fixProviderAmazon",  methods = ['POST'])
def fixProviderAmazon():
    actions = ["MVSHUB.fixProviderAmazon"]
    logger.info("fixProviderAmazon req=> {0}".format( str(request.data) ))
    response = UsersService.fixProviderAmazon(request)
    logger.info("fixProviderAmazon res=> {0}".format( str(response) ))
    return response

@app.route("/addProviderAmazon", methods = ['POST'])
def addProviderAmazon():
    logger.info("addProviderAmazon req=> {0}".format(str(request.data)))
    response = UsersService.addProviderAmazon(request)
    logger.info("addProviderAmazon res=> {0}".format(str(response)))
    return response

# HANDLE ERROR

@app.errorhandler(HTTPException)
def page_error(e):
    response = ResponseDTO()
    response.code = e.code
    response.description = e.name
    return response.getJSON()
