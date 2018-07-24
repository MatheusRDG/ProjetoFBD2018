#Arquivo que cria conexão com o banco de dados e executa as Query's

import pymysql
from pymysql import MySQLError

class Banco:

    def __init__(self,host,user,password,database):
        self.CONNECTION = pymysql.connect(host,user,password,database)
        self.CURSOR = self.CONNECTION.cursor()

    def select(self,querySql):
        try:
            self.CURSOR.execute(querySql)
            return self.CURSOR.fetchall()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))

    def insert(self,querySql):
        try:
            self.CURSOR.execute(querySql)
            self.CONNECTION.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))

    def delete(self,querySql):
        try:
            self.CURSOR.execute(querySql)
            self.CONNECTION.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))

    def update(self,querySql):
        try:
            self.CURSOR.execute(querySql)
            self.CONNECTION.commit()
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))