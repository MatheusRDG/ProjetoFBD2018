class Habilitacao:
    def __init__(self, codigo_servico, matricula_empregado):
        self._codigo_servico = codigo_servico
        self._matricula_empregado = matricula_empregado

    def getCodigoServico(self):
        return self._codigo_servico

    def getMatriculaEmpregado(self):
        return self._matricula_empregado

    def setCodigoServico(self, codigo_servico):
        self._codigo_servico = codigo_servico

    def setMatriculaEmpregado(self, matricula_empregado):
        self._matricula_empregado = matricula_empregado