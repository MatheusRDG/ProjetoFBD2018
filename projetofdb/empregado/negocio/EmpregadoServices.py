from infraestrutura.banco.BancoDados import Banco
from pymysql import MySQLError

class EmpregadoServices:

    def __init__(self):
        self.connection = Banco("localhost", "root", "", "servicos_limpeza")

    def inserirEmpregado(self, empregado):
        try:
            self.connection.insert("INSERT INTO empregado VALUES (%s, %s)" %(empregado.getMatricula(), "'" + empregado.getNome() + "'"))
        except MySQLError as e:
            return e

    def deletarEmpregado(self, empregado):
        try:
            self.connection.delete("DELETE FROM empregado WHERE matricula = " + empregado.getMatricula())
        except MySQLError as e:
            return e

    def atualizarEmpregado(self, matricula, empregado):
        try:
            self.connection.update("UPDATE empregado SET matricula = %s, nome = %s WHERE matricula = %s" % (empregado.getMatricula(), "'" + empregado.getNome() + "'", matricula))
        except MySQLError as e:
            return e

    def listarEmpregados(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e