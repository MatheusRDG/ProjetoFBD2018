class Empregado(object):
    def __init__(self, matricula, nome):
        self._matricula = matricula
        self._nome = nome

    def setMatricula(self, matricula):
        self._matricula = matricula

    def setNome(self, nome):
        self._nome = nome

    def getMatricula(self):
        return self._matricula

    def getNome(self):
        return self._nome