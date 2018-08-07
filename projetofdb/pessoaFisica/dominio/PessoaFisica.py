class PessoaFisica:
    def __init__(self, codigo_cliente, cpf, nome):
        self._codigo_cliente = codigo_cliente
        self._cpf = cpf
        self._nome = nome

    def getCodigoCliente(self):
        return self._codigo_cliente

    def getCpf(self):
        return self._cpf

    def getNome(self):
        return self._nome

    def setCodigoCliente(self, codigo_cliente):
        self._codigo_cliente = codigo_cliente

    def setCpf(self, cpf):
        self._cpf = cpf

    def setNome(self, nome):
        self._nome = nome