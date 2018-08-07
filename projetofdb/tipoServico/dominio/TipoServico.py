class TipoServico:
    def __init__(self, codigo, descricao, duracao_m2, valor_m2):
        self._codigo = codigo
        self._descricao = descricao
        self._duracao_m2 = duracao_m2
        self._valor_m2 = valor_m2

    def setCodigo(self, codigo):
        self._codigo = codigo

    def setDescricao(self, descricao):
        self._descricao = descricao

    def setDuracaoM2(self, duracao_m2):
        self._duracao_m2 = duracao_m2

    def setValorM2(self, valor_m2):
        self._valor_m2 = valor_m2

    def getCodigo(self):
        return self._codigo

    def getDescricao(self):
        return self._descricao

    def getDuracaoM2(self):
        return self._duracao_m2

    def getValorM2(self):
        return self._valor_m2