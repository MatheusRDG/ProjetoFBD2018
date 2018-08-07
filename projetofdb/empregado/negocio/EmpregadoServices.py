from infraestrutura.banco import BancoDados

class EmpregadoServices:

    def __init__(self):
        self.connection = BancoDados.Banco("localhost", "root", "", "servicos_limpeza")
        self.boolean = None

    def inserirEmpregado(self, empregado):
        try:
            self.connection.insert("INSERT INTO empregado VALUES (" + empregado.getMatricula() + "," + "'" + empregado.getNome() + "'" + ")")
        except Exception as e:
            return e.args[0]

    def deletarEmpregado(self, empregado):
        try:
            self.connection.delete("DELETE FROM empregado WHERE matricula = " + empregado.getMatricula())
        except Exception as e:
            return e

    def listarEmpregados(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except Exception as e:
            print('Got error {!r}, errno is {}'.format(e, e.args[0]))