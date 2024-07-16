import oracledb
import os
import logging

class ConnectionOracle:
    def getConnection_PayServices():
        mydb = None
        try:
            mydb = oracledb.connect(
                user = os.getenv('CONNECTION_ORACLE_PAYSERVICES_USER'),
                password = os.getenv('CONNECTION_ORACLE_PAYSERVICES_PASS'),
                dsn = os.getenv('CONNECTION_ORACLE_PAYSERVICES_DSN'),
                encoding = 'UTF-8'
            )
            return mydb
        except Exception as ex:
            mydb = None
            return mydb
        
    def getConnection_Aprdbprod():
        mydb = None
        try:
            mydb = oracledb.connect(
                user = os.getenv('CONNECTION_ORACLE_APRDBPROD_USER'),
                password = os.getenv('CONNECTION_ORACLE_APRDBPROD_PASS'),
                dsn = os.getenv('CONNECTION_ORACLE_APRDBPROD_DSN'),
                encoding = 'UTF-8'
            )
            return mydb
        except Exception as exc:
            logging.error("getConnection_Aprdbprod:" + str(exc) + "\n\n\n")
            mydb = None
            return mydb