from infraestrutura.banco import BancoDados
from pymysql import MySQLError

class TipoServicoServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")

    def inserirTipoServico(self, tipoServico):
        try:
            self.connection.insert("INSERT INTO tipo_servico VALUES (%s, %s, %s, %s)" %(tipoServico.getCodigo(), "'" + tipoServico.getDescricao() + "'", tipoServico.getDuracaoM2(), tipoServico.getValorM2()))
        except MySQLError as e:
            return e

    def removerTipoServico(self, tipoServico):
        try:
            self.connection.delete("DELETE FROM tipo_servico WHERE codigo = " + tipoServico.getCodigo())
        except MySQLError as e:
            return e

    def atualizarTipoServico(self, codigo, tipoServicoAtual):
        try:
            self.connection.update("UPDATE tipo_servico SET descricao = %s, duracao_m2 = %s, valor_m2 = %s WHERE codigo = %s"
                                   %("'"+tipoServicoAtual.getDescricao()+"'", tipoServicoAtual.getDuracaoM2(), tipoServicoAtual.getValorM2(),codigo))
        except MySQLError as e:

            return e

    def listarTipos(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e
