from infraestrutura.banco.BancoDados import Banco
from pymysql import MySQLError

class PedidoServices:

    def __init__(self):
        self.connection = Banco("localhost", "root", "", "servicos_limpeza")

    def inserirPedido(self, pedido):
        try:
            atributos = "('" + pedido.getNumero() + "'" + "," + "'" + pedido.getCodigoCliente() + "'" + "," + "'" + pedido.getDataAbertura() + "'" + "," + "'" + pedido.getLocal() + "'" + "," + "'" + pedido.getDataRealizacao() + "'" + ")"
            self.connection.insert("INSERT INTO pedido VALUES " + atributos)
        except MySQLError as e:
            return e

    def removerPedido(self, pedido):
        try:
            self.connection.delete("DELETE FROM pedido WHERE numero = " + pedido.getNumero())
        except MySQLError as e:
            return e

    def atualizarPedido(self, numero, pedido):
        try:
            if pedido.getCodigoCliente() == "None":
                pedido.setCodigoCliente("null")
            self.connection.update("UPDATE pedido SET codigo_cliente = %s, data_abertura = %s, local = %s, data_realizacao = %s WHERE numero = %s"
                                   %(pedido.getCodigoCliente(),"'" + pedido.getDataAbertura() + "'","'" + pedido.getLocal() + "'",
                                      "'" + pedido.getDataRealizacao() + "'", numero))
        except MySQLError as e:
            return e

    def listarPedidos(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e