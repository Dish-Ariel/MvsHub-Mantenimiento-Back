from flask import Flask
from flask import request
from dotenv import load_dotenv
from werkzeug.exceptions import HTTPException
from service.suscribers import UsersService
from dto.ResponseDTO import ResponseDTO

app = Flask(__name__)
load_dotenv()

@app.route("/getSuscriber/<string:idOrEmail>", methods = ['GET'])
def getSuscriberEmail(idOrEmail):
    return UsersService.getSuscriber(idOrEmail)
    #return {"actionDummy":"Geted"}

@app.route("/updateSuscriberEmail", methods = ['POST'])
def updateSuscriberEmail():
    return UsersService.updateSuscriberEmail(request)
    #return {"actionDummy":"Updated"}

@app.route("/deleteSuscriberEmail", methods = ['POST'])
def deleteSuscriberEmail():
    #return UsersService.deleteSuscriber(request)
    return {"actionDummy":"deleted"}

@app.route("/getStatus",  methods = ['GET'])
def getStatus():
    
    return {"statusDummy":"1"}

# HANDLE ERROR

@app.errorhandler(HTTPException)
def page_error(e):
    response = ResponseDTO()
    response.code = e.code
    response.description = e.name
    return response.getJSON()
