import urllib
from urllib import parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Connector():
    def __init__(self, args):
        self.__driver = args.driver
        self.__server = args.server
        self.__uid = args.uid
        self.__pwd = args.pwd
        self.__database = args.db
        self.base = Base
        self.engine_url_to_server = self.__get_engine_url()
        self.engine_url_to_db = self.__get_engine_url(self.__database)

    def create_database(self):
        if self.__check_db_exist(self.__database):
            return
        engine = create_engine(self.__get_engine_url())
        engine.execute(f"create database {self.__database}")

    def __get_list_dbs(self):
        engine = create_engine(self.__get_engine_url())
        list = []
        for item in engine.execute('SELECT name FROM sys.databases').fetchall():
            list.append(item[0])
        return list

    def __check_db_exist(self, db_name: str):
        return db_name in self.__get_list_dbs()


    def __get_engine_url(self, db_name: str = None):
        if db_name:
            return "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(f"DRIVER={self.__driver};"
                                                                              f"SERVER={self.__server};"
                                                                              f"DATABASE={self.__database};"
                                                                              f"UID={self.__uid};PWD={self.__pwd}")
        else:
            return "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(f"DRIVER={self.__driver};"
                                                                              f"SERVER={self.__server};"
                                                                              f"UID={self.__uid};"
                                                                              f"PWD={self.__pwd}")

    def get_engine(self):
        return create_engine(self.engine_url_to_db)

