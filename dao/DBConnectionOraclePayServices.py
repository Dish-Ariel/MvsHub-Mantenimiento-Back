import cx_Oracle
import os
class ConnectionOracle:
    def getConnection_PayServices():
        mydb = None
        try:
            mydb = cx_Oracle.connect(
                user = os.getenv('CONNECTION_ORACLE_PAYSERVICES_USER'),
                password = os.getenv('CONNECTION_ORACLE_PAYSERVICES_PASS'),
                dsn = os.getenv('CONNECTION_ORACLE_PAYSERVICES_DSN'),
                encoding = 'UTF-8'
            )
            return mydb
        except Exception as ex:
            mydb = None
            return mydb