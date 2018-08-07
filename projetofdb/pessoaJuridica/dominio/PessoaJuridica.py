class PessoaJuridica:
    def __init__(self, codigo_cliente, cnpj, razao_social):
        self._codigo_cliente = codigo_cliente
        self._cnpj = cnpj
        self._razao_social = razao_social

    def setCodigoCliente(self, codigo_cliente):
        self._codigo_cliente = codigo_cliente

    def setCnpj(self, cnpj):
        self._cnpj = cnpj

    def setRazaoSocial(self, razao_social):
        self._razao_social = razao_social

    def getCodigoCliente(self):
        return self._codigo_cliente

    def getCnpj(self):
        return self._cnpj

    def getRazaoSocial(self):
        return self._razao_social
