from infraestrutura.banco.BancoDados import Banco

class PedidoServices:

    def __init__(self):
        self.connection = Banco("localhost", "root", "", "servicos_limpeza")

    def inserirPedido(self, pedido):
        try:
            atributos = "('" + pedido.getNumero() + "'" + "," + "'" + pedido.getCodigoCliente() + "'" + "," + "'" + pedido.getDataAbertura() + "'" + "," + "'" + pedido.getLocal() + "'" + "," + "'" + pedido.getDataRealizacao() + "'" + ")"
            self.connection.insert("INSERT INTO pedido VALUES " + atributos)
        except Exception as e:
            return e

    def removerPedido(self, pedido):
        try:
            self.connection.delete("DELETE FROM pedido WHERE numero = " + pedido.getNumero())
        except Exception as e:
            return e

    def listarPedidos(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except Exception as e:
            return e