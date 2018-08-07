class Alocacao:
    def __init__(self, matricula_empregado, codigo_servico, numero_pedido):
        self._matricula_empregado = matricula_empregado
        self._codigo_servico = codigo_servico
        self._numero_pedido = numero_pedido

    def setMatriculaEmpregado(self, matricula_empregado):
        self._matricula_empregado = matricula_empregado

    def setCodigoServico(self, codigo_servico):
        self._codigo_servico = codigo_servico

    def setNumeroPedido(self, numero_pedido):
        self._numero_pedido = numero_pedido

    def getMatriculaEmpregado(self):
        return self._matricula_empregado

    def getCodigoServico(self):
        return self._codigo_servico

    def getNumeroPedido(self):
        return self._numero_pedido
