from infraestrutura.banco import BancoDados


class EmpregadoServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")
        self.boolean = None

    def inserirEmpregado(self, query):
        try:
            self.connection.insert(query)
        except Exception as e:
            return e.args[0]

    def deletarEmpregado(self, query):
        return self.connection.delete(query)

    def selectALL(self, query):
        try:
            return self.connection.selectALL(query)
        except Exception as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))

    """
        def insertEmpregado(self, query):
        try:
            self.connection.insert(query)
        except Exception as e:
            if e.args[0] == 1062:
                return "Empregado já cadastrado no sistema"
            if e.args[0] == 1406:
                return "Matrícula: máximo de 11 caracteres\nNome: máximo de 100 caracteres"
    """