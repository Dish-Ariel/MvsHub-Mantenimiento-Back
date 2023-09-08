from dao.DBConnectionOraclePayServices import ConnectionOracle
import logging

class QuerierAprdb:
    def updateSuscriberRTFake(suscriberNumber):
        conexion = None
        result1 = 0

        try:
            conexion = ConnectionOracle.getConnection_Aprdbprod()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE T06VENCIMIENTOOFERTASTREAMINGDIGITAL SET FORMA_PAGO = 'Recibo Telmex Fake' WHERE NUMERO_SUSCRIPTOR IN ('%s')", suscriberNumber)
                result1 = cursor.rowcount
                cursor.execute("UPDATE T05VENCIMIENTOOFERTASTREAMING SET FECHA_VENCIMIENTO = SYSDATE -1 WHERE NUMERO_SUSCRIPTOR IN ('%s')", suscriberNumber)
                result2 = cursor.rowcount
        except Exception as exc:
            logging.error("updateSuscriberRTFake:" + str(exc) + "\n\n\n")
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}
            
        if result1 == 1 and result2 == 1: 
            conexion.commit()
            conexion.close()
            return "commited"
        else:
            conexion.close()
            return {"result":"error","message":"non-result","t06 rows updated":result1,"t05 rows updated":result2 }
    
    def checkSuscriberRTFake(idClienteSiebel):
        conexion = None
        suscriber = 0
        try:
            conexion = ConnectionOracle.getConnection_Aprdbprod()
            with conexion.cursor() as cursor:
                query = ("SELECT * FROM PAPVD.T05VENCIMIENTOOFERTASTREAMING tv WHERE NUMERO_SUSCRIPTOR = '{}'".format(idClienteSiebel))
                cursor.execute(query)
                suscriber = cursor.fetchall()

            conexion.close()
        except Exception as exc:
            logging.error("checkSuscriberRTFake:" + str(exc) + "\n\n\n")
            if conexion != None:
                conexion.close()
            return "none"
             
        if len(suscriber) > 0: 
            return suscriber
        else:
            return "none"
        