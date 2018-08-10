from infraestrutura.banco.BancoDados import Banco
from pymysql import MySQLError

class ClienteServices:

    def __init__(self):
        self.connection = Banco("localhost", "root", "", "servicos_limpeza")

    def inserirCliente(self, cliente):
        try:
            self.connection.insert(("INSERT INTO cliente VALUES (%s,%s,'" + cliente.getEndereco() + "'" + ")") %(cliente.getCodigo(), cliente.getTelefone()))
        except MySQLError as e:
            return e

    def removerCliente(self, cliente):
        try:
            self.connection.delete("DELETE FROM cliente WHERE codigo = " + cliente.getCodigo())
        except MySQLError as e:
            return e

    def atualizarCliente(self, codigo, cliente):
        try:
            self.connection.update("UPDATE cliente SET codigo = %s, telefone = %s, endereco = %s WHERE codigo = %s"
                                   %(cliente.getCodigo(), "'" + cliente.getTelefone() + "'", "'" + cliente.getEndereco() + "'", codigo))
        except MySQLError as e:
            print(e)
            return e

    def listarClientes(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e