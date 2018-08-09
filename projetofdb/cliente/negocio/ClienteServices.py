from infraestrutura.banco.BancoDados import Banco
from pymysql import MySQLError

class ClienteServices:

    def __init__(self):
        self.connection = Banco("localhost", "root", "", "servicos_limpeza")

    def inserirCliente(self, cliente):
        try:
            endereco = cliente.getEndereco()
            if endereco == ", . , .":
                endereco = "null"
            self.connection.insert(("INSERT INTO cliente VALUES (%s,%s,'" + endereco + "'" + ")") %(cliente.getCodigo(), cliente.getTelefone()))
        except MySQLError as e:
            return e

    def removerCliente(self, cliente):
        try:
            self.connection.delete("DELETE FROM cliente WHERE codigo = " + cliente.getCodigo())
        except MySQLError as e:
            return e

    def listarClientes(self, query):
        try:
            return self.connection.selecionarTodos(query)
        except MySQLError as e:
            return e