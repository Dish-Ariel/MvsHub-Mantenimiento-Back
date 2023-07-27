import pymysql
import os

class ConnectionMysqlDishPlus:
    def getConnection():
        mydb = None
        try:
            mydb = pymysql.connect(host = os.getenv('CONNECTION_MYSQL_DISHPLUS_HOST'),
                            port = int (os.getenv('CONNECTION_MYSQL_DISHPLUS_PORT')),
                            user = os.getenv('CONNECTION_MYSQL_DISHPLUS_USER'),
                            password = os.getenv('CONNECTION_MYSQL_DISHPLUS_PASS'),
                            db = os.getenv('CONNECTION_MYSQL_DISHPLUS_SCHM'),
                            cursorclass=pymysql.cursors.DictCursor,
                            charset="utf8",
                            use_unicode=True)
            return mydb
        except Exception as ex:
            mydb = None
            return mydb

                                
    def getTestConnection():
        return pymysql.connect(host = os.getenv('CONNECTION_TEST_MYSQL_DISHPLUS_HOST'),
                                port = int (os.getenv('CONNECTION_TEST_MYSQL_DISHPLUS_PORT')),
                                user = os.getenv('CONNECTION_TEST_MYSQL_DISHPLUS_USER'),
                                password = os.getenv('CONNECTION_TEST_MYSQL_DISHPLUS_PASS'),
                                db = os.getenv('CONNECTION_TEST_MYSQL_DISHPLUS_SCHM'),
                                cursorclass=pymysql.cursors.DictCursor,
                                charset="utf8",
                                use_unicode=True)
    
    def getConnection_Cache_pagos():
        return pymysql.connect(host = os.getenv('CONNECTION_MYSQL_CACHEPAGOS_HOST'),
                                port = int (os.getenv('CONNECTION_MYSQL_CACHEPAGOS_PORT')),
                                user = os.getenv('CONNECTION_MYSQL_CACHEPAGOS_USER'),
                                password = os.getenv('CONNECTION_MYSQL_CACHEPAGOS_PASS'),
                                db = os.getenv('CONNECTION_MYSQL_CACHEPAGOS_SCHM'),
                                cursorclass=pymysql.cursors.DictCursor,
                                charset="utf8",
                                use_unicode=True)
