from dao.DBConnectionMongoControl import ConnectionMongoControl
from bson.objectid import ObjectId
import datetime

class QuerierControl:
    def getSuscribersRT(dateFrom,dateTo):
        collectionSuscribersRT = ConnectionMongoControl.getCollection("SuscribersRT")
        query = {"createdAt":{"$gte":datetime.date.isoformat(dateFrom),"$lt":datetime.date.isoformat(dateTo)}}
        collectionSuscribersRT.find(query)

    def addSuscribersRT(idClienteSiebel,date,message):
        collectionSuscribersRT = ConnectionMongoControl.getCollection("SuscribersRT")
        item = {"createdAt":date,"idClienteSiebel":idClienteSiebel,"message":message}
        collectionSuscribersRT.insert_one(item)

    def addLog(request,response,date):
        mydb = ConnectionMongoControl.getDatabase("MTO_LOGS")
        collectionLogs = mydb["Logs"]
        item = {"request":request,"response":response,"date":date, "app": "MVSHUB_MTO"}
        collectionLogs.insert_one(item)

    def getUserPermissions(name,pin):
        mydb = ConnectionMongoControl.getDatabase("MTO_USERS")
        collectionUsers = mydb["Users"]
        query = {"pin":pin, "name":name}
        rs = collectionUsers.find_one(query)
        return rs #LISTA DE PERMISOS