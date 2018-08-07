class ItemPedido:
    def __init__(self, codigo_servico, numero_pedido, metragem):
        self._codigo_servico = codigo_servico
        self._numero_pedido = numero_pedido
        self._metragem = metragem

    def getCodigoServico(self):
        return self._codigo_servico

    def getNumeroPedido(self):
        return self._numero_pedido

    def getMetragem(self):
        return self._metragem

    def setCodigoServico(self, codigo_servico):
        self._codigo_servico = codigo_servico

    def setNumeroPedido(self, numero_pedido):
        self._numero_pedido = numero_pedido

    def setMetragem(self, metragem):
        self._metragem = metragem