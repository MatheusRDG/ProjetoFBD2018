#Arquivo que cria conexão com o banco de dados e executa as Query's

import pymysql
from pymysql import MySQLError

connection = pymysql.connect(host='localhost',user='root',password='',database = 'servicos_limpeza')
cursor = connection.cursor()

def select(querySql):
    try:
        cursor.execute(querySql)
        return cursor.fetchall()
    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))

def insert(querySql):
    try:
        cursor.execute(querySql)
        connection.commit()
    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))

def delete(querySql):
    try:
        cursor.execute(querySql)
        connection.commit()
    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))

def update(querySql):
    try:
        cursor.execute(querySql)
        connection.commit()
    except MySQLError as e:
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))