from dao.DBConnectionMySqlDishPlus import ConnectionMysqlDishPlus
import logging

class QuerierAmazonPrime:

    def getSuscriber(idOrEmail):
        conexion = None
        suscriber = []

        try:
            conexion = ConnectionMysqlDishPlus.getConnection_AmazonPrime()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM suscriptors s WHERE id_cliente = %s", (idOrEmail))
                suscriber = cursor.fetchall()
            conexion.close()
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error getConnection_AmazonPrime","message":exc}
        
        if len(suscriber) == 1: 
            return suscriber
        else:
            return "none"
        
    def deleteSuscriber(idSiebel):
        conexion = None
        
        try:
            conexion = ConnectionMysqlDishPlus.getConnection_AmazonPrime()
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM suscriptors WHERE id_cliente = %s", (idSiebel))
                response = cursor.fetchall()
                result = cursor.rowcount
                
        except Exception as exc:
            if conexion != None:
                conexion.close()
            print("getConnection_AmazonPrime exc:{0}".format(exc))
            return "error"
            {"result":"error getConnection_AmazonPrime", "message":exc}
        
        #response = number of logs in table customer_cards_domiciliation        
        if result == 1:
            # commit and close is previus of send body to lambda, to give chance to get logs of body well
            #CRITIC commit the deletion (in case of)
            #MANUAL 
            conexion.commit()
            conexion.close()
            
            return "commited"
        else:
            print("deletions:{0}".format(result))
            conexion.close()
            return "none"
