from infraestrutura.banco.BancoDados import Banco
from pymysql import MySQLError

class HabilitacaoServices:

    def __init__(self):
        self.connection = Banco()

    def inserirHabilitacao(self, habilitacao):
        try:
            self.connection.insert("INSERT INTO habilitacao VALUES (%s, %s)" %(habilitacao.getCodigoServico(), habilitacao.getMatriculaEmpregado()))
        except MySQLError as e:
            return e

    def removerHabilitacao(self, habilitacao):
        try:
            self.connection.delete("DELETE FROM habilitacao WHERE codigo_servico = %s AND matricula_empregado = %s" %(habilitacao.getCodigoServico(), habilitacao.getMatriculaEmpregado()))
        except MySQLError as e:
            return e

    def listarHabilitacao(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e