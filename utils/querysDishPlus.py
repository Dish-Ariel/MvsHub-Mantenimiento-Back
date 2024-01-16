from dao.DBConnectionMongoControl import ConnectionMongoControl
from dao.DBConnectionMySqlDishPlus import ConnectionMysqlDishPlus
import logging

class QuerierDishPlus:
    def getSuscribersRT(dateFrom,dateTo):
        dateFormedFrom = str(dateFrom) + " 00:00:00"
        dateFormedTo = str(dateTo) + " 23:59:59"

        conexion = None
        suscribers = []

        try:
            conexion = ConnectionMysqlDishPlus.getConnection()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM creacion_siebel_pendiente csp, customer_dish_plus cdp WHERE csp.correo = cdp.email and csp.pago_suscripcion IN ('Recibo Telmex') and fecha > %s and fecha < %s ORDER BY fecha DESC", (dateFormedFrom,dateFormedTo))
                suscribers = cursor.fetchall()
            conexion.close()
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}
        
        if len(suscribers) > 0: 
            return suscribers
        else:
            return "none"
        
    def getSuscriber(kind,idOrEmail):
        conexion = None
        suscriber = []

        try:
            conexion = ConnectionMysqlDishPlus.getConnection()
            with conexion.cursor() as cursor:
                if kind == "email":
                    cursor.execute("SELECT * FROM customer_dish_plus cdp, detail_customer dc WHERE cdp.folio = dc.folio AND cdp.email = %s", (idOrEmail))
                else:
                    cursor.execute("SELECT * FROM customer_dish_plus cdp, detail_customer dc WHERE cdp.folio = dc.folio AND cdp.id_customer= %s", (idOrEmail))
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
    
    def validate_sub(sub):
        conexion = None
        result = 0
        try:
            conexion = ConnectionMysqlDishPlus.getConnection()
            with conexion.cursor() as cursor:
                
                cursor.execute("SELECT count(email) FROM customer_dish_plus WHERE username = %s",sub)
                result = cursor.fetchall()
                
            conexion.close()
        except Exception as exc:
            
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}
        
        if result[0]['count(email)'] >= 1: 
            
            return result
        else:

            return "none"
    
    def update_username(sub, email):
        conexion = None
        result = 0
        try:
            conexion = ConnectionMysqlDishPlus.getConnection()
            with conexion.cursor() as cursor:
                cursor.execute("UPDATE customer_dish_plus SET username = %s WHERE email = %s",(str(sub),str(email)))
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
    
    def delete_domiciliation(folio):
        conexion = None
        
        try:
            conexion = ConnectionMysqlDishPlus.getConnection()

            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM dishplus.customer_cards_domiciliation WHERE folio = %s",(str(folio)))
                response = cursor.fetchall()
                result = 0
                if len(response) > 0:
                    cursor.execute("DELETE FROM dishplus.customer_cards_domiciliation where folio = %s",(str(folio)))
                    result = cursor.rowcount
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error", "message":exc}
        #response = number of logs in table customer_cards_domiciliation        
        if result == len(response) and result > 0:
            conexion.commit()
            conexion.close()
            return "commited"
        else:
            conexion.close()
            return "none"
    
    def check_payments(id_cliente_siebel, id_customer):
        conexion = None
        if id_cliente_siebel == 0 and id_customer == 0:
            return "none"
        elif id_cliente_siebel == 0:
            id_cliente_siebel = id_customer

        try:
            
            conexion = ConnectionMysqlDishPlus.getConnection_Cache_pagos()
            
            with conexion.cursor() as cursor:
        
                cursor.execute("SELECT * FROM transacciones_recibidas_vicomm trv where cliente = %s OR cliente = %s",(id_cliente_siebel,id_customer))
                vicomm_r = cursor.fetchall()
                cursor.execute("SELECT * FROM t06ctrl_movimientos_inbox_vicomm tcmiv WHERE cliente = %s OR cliente = %s",(id_cliente_siebel,id_customer) )
                vicomm = cursor.fetchall()
                cursor.execute("SELECT * FROM t04ctrl_movimientos_inboxoracleV2_dishplus WHERE t04_cliente=%s OR t04_cliente = %s",(id_cliente_siebel,id_customer))
                t04ctrl = cursor.fetchall()
                cursor.execute("SELECT * FROM t06ctrl_movimientos_inboxOC_PayPal_mvshub where t06cliente = %s OR t06cliente = %s",(id_cliente_siebel,id_customer) )
                paypal = cursor.fetchall()
                conexion.close()
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}
        
        if len(vicomm_r) or len(vicomm) or len(t04ctrl) or len(paypal) >= 1:
            return "Payment exists"
        else:
            return "none"
    
    def delete_cache_pagos(phone_number,id_customer, id_cliente_siebel):
        conexion = None
        if id_cliente_siebel == 0:
            id_cliente_siebel = id_customer
        
        try : 
           
            conexion = ConnectionMysqlDishPlus.getConnection_Cache_pagos()
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM ctrl_mediosexternosV2_dishplus WHERE n_talon2 = %s AND c_cliente = %s OR c_cliente = %s",(phone_number,id_customer,id_cliente_siebel))
                payment = cursor.rowcount
                
        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}

        if payment == 1:
            conexion.commit()
            conexion.close()
            return "commited"
        else:
            conexion.close()
            return "none"

    def delete_from_siebel(email, id_customer):
        conexion = None
    
        try:
            conexion = ConnectionMysqlDishPlus.getConnection()
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM creacion_siebel_pendiente where correo IN (%s) or cliente = %s",(email,id_customer))
                delete = cursor.rowcount

        except Exception as exc:
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}
        
        if delete == 1:
            conexion.commit()
            conexion.close()
            return "commited"
        else:
            conexion.close()
            return "none"
         
    
    
    def disable_amazon_prime(idClienteSiebel,reason,ticket):
        conexion = None
        try :      
            conexion = ConnectionMysqlDishPlus.getConnection_AmazonPrime()
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO cancelaciones_operaciones (cliente, descripcion, estatus, ticket) VALUES(%s, %s,'POR_DESPACHAR', %s)",(idClienteSiebel,reason,ticket))
                inserted = cursor.rowcount
                
        except Exception as exc:
            logging.error("disable_amazon_prime:" + str(exc) + "\n\n\n")
            if conexion != None:
                conexion.close()
            return {"result":"error","message":exc}

        if inserted == 1:
            conexion.commit()
            conexion.close()
            return "commited"
        else:
            conexion.close()
            return "none"

    def check_amazon_prime(idClienteSiebel):
        conexion = None
        try :      
            conexion = ConnectionMysqlDishPlus.getConnection_AmazonPrime()
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM cancelaciones_operaciones WHERE cliente = '%s'",idClienteSiebel)
                payment = cursor.fetchall()
                conexion.close()
                
        except Exception as exc:
            logging.error("check_amazon_prime:" + str(exc) + "\n\n\n")
            if conexion != None:
                conexion.close()
            return "exist"

        if len(payment) >= 1:
            return "exist"
        else:
            return "none"    