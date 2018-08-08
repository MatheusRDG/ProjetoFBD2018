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
