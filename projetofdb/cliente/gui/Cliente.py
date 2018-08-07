class Cliente:
    def __init__(self, codigo, telefone, endereco):
        self._codigo = codigo
        self._telefone = telefone
        self._endereco = endereco

    def setCodigo(self, codigo):
        self._codigo = codigo

    def setTetelefone(self, telefone):
        self._telefone = telefone

    def setEndereco(self, endereco):
        self._endereco = endereco

    def getCodigo(self):
        return self._codigo

    def getTelefone(self):
        return self._telefone

    def getEndereco(self):
        return self._endereco