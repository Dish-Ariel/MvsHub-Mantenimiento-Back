from dao.DBConnectionMongoControl import ConnectionMongoControl
from dao.DBConnectionMySqlDishPlus import ConnectionMysqlDishPlus

class QuerierDishPlus:
    def getSuscriber(kind,idOrEmail):
        conexion = None
        suscriber = []

        try:
            conexion = ConnectionMysqlDishPlus.getConnection()
            with conexion.cursor() as cursor:
                if kind == "email":
                    cursor.execute("SELECT * FROM customer_dish_plus cdp, detail_customer dc WHERE cdp.folio = dc.folio AND cdp.email = %s", (idOrEmail))
                else:
                    cursor.execute("SELECT * FROM customer_dish_plus cdp, detail_customer dc WHERE cdp.folio = dc.folio AND cdp.id_cliente_siebel = %s", (idOrEmail))
                suscriber = cursor.fetchall()
            conexion.close()
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}

        
        if len(suscriber) == 1: 
            return suscriber
        else:
            return "none"
        
    def countSuscribers(kind,idOrEmail):
        conexion = None
        suscriber = []
        
        try:
            conexion = ConnectionMysqlDishPlus.getConnection()
            with conexion.cursor() as cursor:
                if kind == "email":
                    cursor.execute("SELECT * FROM customer_dish_plus WHERE email = %s", (idOrEmail))
                else:
                    cursor.execute("SELECT * FROM customer_dish_plus WHERE id_cliente_siebel = %s", (idOrEmail))
                suscriber = cursor.fetchall()
            conexion.close()
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}

        return len(suscriber)
    

    def getSuscriberLogs(folio):
        conexion = None
        logs = []

        try:
            conexion = ConnectionMysqlDishPlus.getConnection()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM log_suscription WHERE folio = %s", (folio))
                logs = cursor.fetchall()
            conexion.close()
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}

        if len(logs) >= 1: 
            return logs
        else:
            return "none"


    def updateSuscriber(lastEmail,newEmail):
        conexion = None
        result = 0

        try:
            conexion = ConnectionMysqlDishPlus.getConnection()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE customer_dish_plus SET email = %s WHERE email = %s", (newEmail,lastEmail))
                result = cursor.rowcount
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}
            
        if result == 1: 
            conexion.commit()
            conexion.close()
            return "commited"
        else:
            conexion.close()
            return {"result":"ok","message":"non-result"}