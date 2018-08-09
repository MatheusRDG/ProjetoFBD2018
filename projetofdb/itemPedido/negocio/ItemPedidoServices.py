from infraestrutura.banco import BancoDados
from pymysql import MySQLError

class ItemPedidoServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")

    def inserirItemPedido(self, itemPedido):
        try:
            self.connection.insert("INSERT INTO item_pedido VALUES (%s,%s,%s)" %(itemPedido.getCodigoServico(), itemPedido.getNumeroPedido(), itemPedido.getMetragem()))
        except MySQLError as e:
            return e

    def removerItemPedido(self, itemPedido):
        try:
            self.connection.delete("DELETE FROM item_pedido WHERE numero_pedido = %s AND codigo_servico = %s" %(itemPedido.getNumeroPedido(),itemPedido.getCodigoServico()))
        except MySQLError as e:
            return e

    def listarItensPedido(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e