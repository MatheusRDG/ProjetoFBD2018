from infraestrutura.banco import BancoDados

class TipoServicoServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")

    def inserirTipoServico(self, tipoServico):
        try:
            atributos = "('" + tipoServico.getCodigo() + "'" + "," + "'" + tipoServico.getDescricao() + "'" + "," + "'" + tipoServico.getDuracaoM2() \
                        + "'" + "," + "'" + tipoServico.getValorM2() + "'" ")"
            self.connection.insert("INSERT INTO tipo_servico VALUES " + atributos)
        except Exception as e:
            print(e)
            return e

    def removerTipoServico(self, tipoServico):
        try:
            self.connection.delete("DELETE FROM tipo_servico WHERE codigo = " + tipoServico.getCodigo())
        except Exception as e:
            return e

    def listarTipos(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except Exception as e:
            return e
