#Arquivo que cria conexão com o banco de dados e executa as Query's
import pymysql
from pymysql import MySQLError

class Banco:

    def __init__(self):
        self.CONNECTION = pymysql.connect("localhost", "root", "", "servicos_limpeza")
        self.CURSOR = self.CONNECTION.cursor()

    def select(self,querySql):
        try:
            self.CURSOR.execute(querySql)
            return True
        except MySQLError as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))

    def insert(self,querySql):
        self.CURSOR.execute(querySql)
        self.CONNECTION.commit()

    def delete(self,querySql):
        self.CURSOR.execute(querySql)
        self.CONNECTION.commit()

    def update(self,querySql):
        self.CURSOR.execute(querySql)
        self.CONNECTION.commit()

    def selecionarTodos(self, querySql):
        lista = []
        self.CURSOR.execute(querySql)
        for row in self.CURSOR:
            lista.append(row)
        return lista