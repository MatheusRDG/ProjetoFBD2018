from infraestrutura.banco.BancoDados import Banco

class EmpregadoServices:

    def __init__(self):
        self.connection = Banco("localhost", "root", "", "servicos_limpeza")

    def inserirEmpregado(self, empregado):
        try:
            atributos = "('" + empregado.getMatricula() + "'" + "," + "'" + empregado.getNome() + "'" + ")"
            self.connection.insert("INSERT INTO empregado VALUES " + atributos)
        except Exception as e:
            return e

    def deletarEmpregado(self, empregado):
        try:
            self.connection.delete("DELETE FROM empregado WHERE matricula = " + empregado.getMatricula())
        except Exception as e:
            return e

    def listarEmpregados(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except Exception as e:
            return e