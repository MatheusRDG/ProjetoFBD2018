class Pedido:
    def __init__(self, numero, codigo_cliente, data_abertura, local, data_localizacao):
        self._numero = numero
        self._codigo_cliente = codigo_cliente
        self._data_abertura = data_abertura
        self._local = local
        self._data_localizacao = data_localizacao

    def setNumero(self, numero):
        self._numero = numero

    def setCodigoCliente(self, codigo_cliente):
        self._codigo_cliente = codigo_cliente

    def setDataAbertura(self, data_abertura):
        self._data_abertura = data_abertura

    def setLocal(self, local):
        self._local = local

    def setDataLocalizacao(self, data_localizacao):
        self._data_localizacao = data_localizacao

    def getNumero(self):
        return self._numero

    def getCodigoCliente(self):
        return self._codigo_cliente

    def getDataAbertura(self):
        return self._data_abertura

    def getLocal(self):
        return self._local

    def getDataLocalizacao(self):
        return self._data_localizacao