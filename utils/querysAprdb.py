from dao.DBConnectionOraclePayServices import ConnectionOracle

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
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}
            
        if result1 == 1 and result2 == 1: 
            conexion.commit()
            conexion.close()
            return "commited"
        else:
            conexion.close()
            return {"result":"ok","message":"non-result","t06 rows updated":result1,"t05 rows updated":result2 }
    
    def checkSuscriberRTFake(idClienteSiebel):
        conexion = None
        suscriber = 0
        try:
            conexion = ConnectionOracle.getConnection_Aprdbprod()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM PAPVD.T05VENCIMIENTOOFERTASTREAMING tv WHERE NUMERO_SUSCRIPTOR = '%s'", idClienteSiebel)
                suscriber = cursor.fetchall()

            conexion.close()
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}
             
        if len(suscriber) > 0: 
            return suscriber
        else:
            return "none"
        