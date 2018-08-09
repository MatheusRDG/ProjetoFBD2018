from infraestrutura.banco.BancoDados import Banco
from pymysql import MySQLError

class AlocacaoServices:

    def __init__(self):
        self.connection = Banco("localhost", "root", "", "servicos_limpeza")

    def inserirAlocacao(self, alocacao):
        try:
            self.connection.insert(("INSERT INTO alocacao VALUES (%s,%s,%s)" %(alocacao.getMatriculaEmpregado(), alocacao.getCodigoServico(), alocacao.getNumeroPedido())))
        except MySQLError as e:
            return e

    def removerAlocacao(self, alocacao):
        try:
            self.connection.delete("DELETE FROM alocacao WHERE matricula_empregado = %s AND codigo_servico = %s AND numero_pedido = %s"
                                   %(alocacao.getMatriculaEmpregado(), alocacao.getCodigoServico(), alocacao.getNumeroPedido()))
        except MySQLError as e:
            return e

    def listarAlocacao(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e